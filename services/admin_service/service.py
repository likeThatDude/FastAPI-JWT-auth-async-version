from typing import Union

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.authenticate.models import User
from services.database.db_connect import get_async_session
from services.authenticate.schemas import UserSchema
from services.admin_service.exeptions import exception_404
from services.celery_app.celery_app import send_email_to_one_user


class AdminService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_user_data(self, user_id) -> UserSchema:
        query = await self.session.execute(select(User).where(User.id == user_id))
        user_data = query.scalar()
        if user_data:
            user = UserSchema.parse_obj(user_data)
            return user
        else:
            return exception_404

    async def send_email(self, user_id) -> dict:
        query = await self.session.execute(select(User).where(User.id == user_id))
        user_data = query.scalar()
        if user_data:
            try:
                result = send_email_to_one_user.delay(user_data.username, user_data.email)
                print(result)
                return {'message': f'Письмо отправлено пользователю {user_data.username}'}
            except Exception:
                return {'message': f'Письмо не получилось отправить пользователю {user_data.username}'}
        else:
            return exception_404
