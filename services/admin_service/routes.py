from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from services.authenticate.service import get_current_user
from services.authenticate.schemas import UserSchema
from services.admin_service.service import AdminService
from services.admin_service.schemas import GetUserForm, MailAnswerSchema, ExceptionSchema, ChangeRoleSchema, \
    UserBanSchema, BanOrUnbannedSchema
from services.admin_service.exeptions import exception_403, exception_500

admin_route = APIRouter(prefix='/admin', tags=['Administrator service'])


@admin_route.post('/send_emails', response_model=Union[MailAnswerSchema, ExceptionSchema])
async def send_mail_to_user(user_id: GetUserForm, user: UserSchema = Depends(get_current_user),
                            service: AdminService = Depends()):
    try:
        if user.role_id != 4:
            return exception_403

        mail_answer = await service.send_email(user_id.id)
        return mail_answer

    except Exception:
        return exception_500


@admin_route.post('/get_user_data', response_model=Union[UserSchema, ExceptionSchema])
async def get_user_data(data_form: GetUserForm, user: UserSchema = Depends(get_current_user),
                        service: AdminService = Depends()):
    try:
        if user.role_id != 4:
            return exception_403

        user_data = await service.get_user_data(data_form.id)
        return user_data
    except Exception:
        return exception_500


@admin_route.post('/change_role', response_model=Union[UserSchema, ExceptionSchema])
async def change_role(data_form: ChangeRoleSchema, user: UserSchema = Depends(get_current_user),
                      service: AdminService = Depends()):
    if user.role_id != 4:
        return exception_403
    user_data = await service.change_role(data_form)
    return user_data


@admin_route.post('/change_ban_status', response_model=Union[UserBanSchema, ExceptionSchema])
async def change_ban_status(user_data: BanOrUnbannedSchema, user: UserSchema = Depends(get_current_user),
                            service: AdminService = Depends()):
    if user.role_id != 4:
        return exception_403
    user_data = await service.change_user_ban(user_data)
    return user_data
