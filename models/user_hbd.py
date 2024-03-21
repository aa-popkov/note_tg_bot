from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, ForeignKey, String, func, delete

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

    @staticmethod
    async def delete_hbd(hbd_id: int) -> bool:
        async with async_session_factory() as session:
            q = delete(UserHappyBirthday).where(UserHappyBirthday.id == hbd_id)
            await session.execute(q)
            await session.flush()
            await session.commit()
            return True

    @staticmethod
    async def get_hbd_by_id(hbd_id: int) -> Optional["UserHappyBirthday"]:
        async with async_session_factory() as session:
            q = select(UserHappyBirthday).where(UserHappyBirthday.id == hbd_id)
            result = await session.execute(q)
            return result.scalar_one_or_none()

    @staticmethod
    async def get_count_by_user(user_id: str) -> int:
        async with async_session_factory() as session:
            q = (
                select(func.count(UserHappyBirthday.user_id))
                .select_from(UserHappyBirthday)
                .where(UserHappyBirthday.user_id == user_id)
            )
            result = await session.execute(q)
            return result.scalar()

    @staticmethod
    async def get_all_hbd_by_user(
        user_id: str, page_num: int = 0
    ) -> Optional[List["UserHappyBirthday"]]:
        async with async_session_factory() as session:
            q = (
                select(UserHappyBirthday)
                .where(UserHappyBirthday.user_id == user_id)
                .order_by(UserHappyBirthday.created_at)
                .limit(5)
                .offset(page_num)
            )
            result = await session.execute(q)
            return result.scalars().all()
