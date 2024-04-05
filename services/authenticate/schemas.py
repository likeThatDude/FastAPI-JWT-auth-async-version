from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    username: str
    email: str


class UserCreateSchema(BaseUserSchema):
    password: str


class UserSchema(BaseUserSchema):
    id: int

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    username: str
    password: str


class CookieResponse(BaseModel):
    token: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'