from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, insert

from .base import Base
from utils.database import async_session_factory


class User(Base):
    tg_id: Mapped[str] = mapped_column(unique=True, index=True)
    phone_num: Mapped[str]
    username: Mapped[Optional[str]]

    def __repr__(self):
        return f"User: \n" f"{self.username}\n" f"{self.phone_num}\n" f"{self.tg_id}\n"

    @staticmethod
    async def add_user(user: "User") -> str:
        async with async_session_factory() as session:
            session.add(user)
            await session.flush()
            await session.commit()
            await session.refresh(user)
            return user.id

    @staticmethod
    async def get_user_by_tg_id(tgid: str) -> Optional["User"]:
        async with async_session_factory() as session:
            query = select(User).where(User.tg_id == tgid)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            return user
