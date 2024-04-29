from typing import Union

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from services.authenticate.models import User
from services.database.db_connect import get_async_session
from services.authenticate.schemas import UserSchema
from services.admin_service.exeptions import exception_404, exception_500, exception_400
from services.celery_app.celery_app import send_email_to_one_user
from services.admin_service.schemas import ChangeRoleSchema, ExceptionSchema, BanOrUnbannedSchema, UserBanSchema


class AdminService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_user_data(self, user_id) -> UserSchema:
        query = await self.session.execute(select(User).where(User.id == user_id))
        user_data = query.scalar()
        if user_data:
            user = UserSchema.from_orm(user_data)
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

    async def change_role(self, new_data: ChangeRoleSchema) -> Union[UserSchema, ExceptionSchema]:
        try:
            query = await self.session.execute(select(User).where(User.id == new_data.user_id))
            data = query.scalar()
            if not data:
                return exception_404
            data.role_id = new_data.role_id
            await self.session.flush()
            new_user_data = UserSchema.from_orm(data)
            await self.session.commit()
            return new_user_data

        except IntegrityError:
            return exception_400
        except Exception:
            return exception_500

    async def change_user_ban(self, user_data: BanOrUnbannedSchema) -> Union[UserBanSchema, ExceptionSchema]:
        try:
            query = await self.session.execute(select(User).where(User.id == user_data.user_id))
            data = query.scalar()
            if not data:
                return exception_404
            data.ban = user_data.status
            await self.session.flush()
            new_user_data = UserBanSchema.from_orm(data)
            await self.session.commit()
            return new_user_data

        except IntegrityError:
            return exception_400
        except Exception:
            return exception_500
