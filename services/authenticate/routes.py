from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from services.authenticate.schemas import UserCreateSchema, TokenSchema, UserSchema, CookieResponse, UserLoginSchema
from services.authenticate.service import AuthService, get_current_user, logout_user

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])


@auth_router.post('/registration', response_model=TokenSchema)
async def sign_up(user_data: UserCreateSchema, service: AuthService = Depends()):
    return await service.registration_new_user(user_data)


@auth_router.post('/login', response_model=CookieResponse)
async def sign_in(form_data: UserLoginSchema, service: AuthService = Depends()):
    return await service.authenticate_user(form_data.username, form_data.password)


@auth_router.get('/user', response_model=UserSchema)
async def get_user(user: UserSchema = Depends(get_current_user)):
    return user


@auth_router.post("/logout")
async def logout():
    return await logout_user()
