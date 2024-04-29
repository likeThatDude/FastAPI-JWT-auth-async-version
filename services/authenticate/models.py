from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.database.db_connect import Base


class User(Base):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(length=20), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False, default=1)
    roles: Mapped[list['Role']] = relationship(back_populates='users')
    ban: Mapped[bool] = mapped_column(nullable=True, default=False)


class Role(Base):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    role_name: Mapped[str] = mapped_column(nullable=False)
    users: Mapped[list['User']] = relationship(back_populates='roles')

