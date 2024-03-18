from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, ForeignKey, String

from utils.database import async_session_factory
from . import User
from .base import Base, created_at, updated_at


class UserHappyBirthday(Base):
    person_name: Mapped[str] = mapped_column(String(40))
    person_birthdate: Mapped[datetime]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    user_id: Mapped[str] = mapped_column(ForeignKey(User.tg_id))

    @staticmethod
    async def add_hbd(user_hbd: "UserHappyBirthday") -> int:
        async with async_session_factory() as session:
            session.add(user_hbd)
            await session.flush()
            await session.commit()
            await session.refresh(user_hbd)
            return user_hbd.id
