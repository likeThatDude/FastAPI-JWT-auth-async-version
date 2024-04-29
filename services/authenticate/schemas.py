from pydantic import BaseModel, ConfigDict


class BaseUserSchema(BaseModel):
    username: str
    email: str


class UserCreateSchema(BaseUserSchema):
    password: str


class UserSchema(BaseUserSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role_id: int


class UserLoginSchema(BaseModel):
    username: str
    password: str


class CookieResponse(BaseModel):
    token: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class ExceptionSchema(BaseModel):
    status_code: int
    detail: str
    headers: dict