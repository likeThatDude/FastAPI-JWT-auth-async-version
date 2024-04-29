from typing import Union

from fastapi import APIRouter, Depends
from services.authenticate.schemas import UserCreateSchema, TokenSchema, UserSchema, CookieResponse, UserLoginSchema, \
    ExceptionSchema
from services.authenticate.service import AuthService, get_current_user, logout_user
from fastapi_cache.decorator import cache

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])


@auth_router.post('/registration', response_model=TokenSchema)
async def sign_up(user_data: UserCreateSchema, service: AuthService = Depends()):
    return await service.registration_new_user(user_data)


@auth_router.post('/login', response_model=Union[CookieResponse, ExceptionSchema])
async def sign_in(form_data: UserLoginSchema, service: AuthService = Depends()):
    return await service.authenticate_user(form_data.username, form_data.password)


@auth_router.post("/logout")
async def logout():
    return await logout_user()


@auth_router.get('/user', response_model=UserSchema)
@cache(expire=30)
async def get_user(user: UserSchema = Depends(get_current_user)):
    return user
