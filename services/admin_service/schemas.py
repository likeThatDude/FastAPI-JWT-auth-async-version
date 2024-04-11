from pydantic import BaseModel


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
