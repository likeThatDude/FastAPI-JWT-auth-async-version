from pydantic import BaseModel, field_validator, ConfigDict


class AdminSchema(BaseModel):
    id: int
    username: str
    email: str
    role_id: int


class GetUserForm(BaseModel):
    id: int


class MailAnswerSchema(BaseModel):
    message: str


class ExceptionSchema(BaseModel):
    status_code: int
    detail: str
    headers: dict


class ChangeRoleSchema(BaseModel):
    user_id: int
    role_id: int

    @classmethod
    @field_validator('role_id')
    def validate_role_id(cls, v):
        if v > 4:
            raise ValueError('role_id должен быть не больше 4')
        return v


class BanOrUnbannedSchema(BaseModel):
    user_id: int
    status: bool


class UserBanSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    ban: bool
