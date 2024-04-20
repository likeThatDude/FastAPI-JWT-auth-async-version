import datetime

import jwt
from jwt import PyJWTError
import bcrypt
from pydantic import ValidationError

from services.authenticate.schemas import UserSchema, TokenSchema, UserCreateSchema
from fastapi.exceptions import HTTPException
from fastapi import status, Depends, Request
from fastapi.responses import JSONResponse
from services.authenticate.models import User
from services.database.db_connect import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import settings


async def get_current_user(user_request: Request) -> UserSchema:
    access_token_cookie = user_request.cookies.get("access_token")
    user = await AuthService.validate_token(access_token_cookie)
    return user


async def logout_user():
    response = JSONResponse(content={"message": "Successfully logged out"})
    response.delete_cookie("access_token")
    return response


class AuthService:
    @classmethod
    async def verify_password(cls, form_password: str, db_hashed_password: str) -> bool:
        return bcrypt.checkpw(form_password.encode('utf-8'), db_hashed_password.encode('utf-8'))

    @classmethod
    async def hashed_password(cls, password) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @classmethod
    async def validate_token(cls, token: str) -> UserSchema:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Sorry yours token not valid :(',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )
        try:
            payload = jwt.decode(token, settings.jwy_public_key, algorithms=[settings.jwt_algorithm])
        except PyJWTError:
            raise exception from None
        user_data = payload.get('user')
        try:
            user = UserSchema.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    async def create_token(cls, user: User) -> TokenSchema:
        user_data = UserSchema(id=user.id, username=user.username, email=user.email, role_id=user.role_id)
        time_now = datetime.datetime.utcnow()
        payload = {
            'iat': time_now,
            'nbf': time_now,
            'exp': time_now + datetime.timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict(),
            'role_id': user_data.role_id
        }
        token = jwt.encode(payload, settings.jwt_private_key, algorithm=settings.jwt_algorithm)
        return TokenSchema(access_token=token)

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def registration_new_user(self, user_data: UserCreateSchema) -> TokenSchema:
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=await self.hashed_password(user_data.password)
        )
        self.session.add(user)
        await self.session.flush()
        token = await self.create_token(user)
        await self.session.commit()
        return token

    async def authenticate_user(self, username: str, password: str) -> JSONResponse:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )
        query = await self.session.execute(select(User).where(User.username == username))
        user = query.scalar()

        if not user:
            raise exception

        if not await self.verify_password(password, user.hashed_password):
            raise exception
        token = await self.create_token(user)
        response = JSONResponse(content={"token": token.access_token})
        response.set_cookie(key="access_token", value=token.access_token)
        return response
