from typing import List, Optional

from sqlalchemy import ForeignKey, String, select, func, delete, update
from sqlalchemy.orm import Mapped, mapped_column

from utils.database import async_session_factory
from .base import Base, created_at, updated_at
from .user import User


class UserNote(Base):
    title: Mapped[str] = mapped_column(String(10))
    text: Mapped[str] = mapped_column(String(3000))
    user_id: Mapped[str] = mapped_column(ForeignKey(User.tg_id))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    file_id: Mapped[Optional[str]] = None

    @staticmethod
    def convert_title(msg_text: str):
        note_title_sym_count = 10
        if len(msg_text.split("\n")[0]) < 10:
            note_title_sym_count = len(msg_text.split("\n")[0])
        return msg_text.split("\n")[0][0:note_title_sym_count]

    @staticmethod
    async def add_note(user_note: "UserNote") -> int:
        async with async_session_factory() as session:
            session.add(user_note)
            await session.flush()
            await session.commit()
            await session.refresh(user_note)
            return user_note.id

    @staticmethod
    async def get_count_by_user(user_id: str) -> int:
        async with async_session_factory() as session:
            q = (
                select(func.count(UserNote.user_id))
                .select_from(UserNote)
                .where(UserNote.user_id == user_id)
            )

            result = await session.execute(q)
            return result.scalar()

    @staticmethod
    async def get_all_notes_by_user(
        user_id: str, page_num: int = 0
    ) -> Optional[List["UserNote"]]:
        async with async_session_factory() as session:
            q = (
                select(UserNote)
                .where(UserNote.user_id == user_id)
                .order_by(UserNote.created_at)
                .limit(5)
                .offset(page_num)
            )
            result = await session.execute(q)
            return result.scalars().all()

    @staticmethod
    async def get_note_by_id(user_id: str, note_id: int) -> "UserNote":
        async with async_session_factory() as session:
            q = select(UserNote).where(
                (UserNote.user_id == user_id) & (UserNote.id == note_id)
            )
            result = await session.execute(q)
            return result.scalar_one()

    @staticmethod
    async def delete_note(note_id: int) -> bool:
        async with async_session_factory() as session:
            q = delete(UserNote).where(UserNote.id == note_id)
            await session.execute(q)
            await session.flush()
            await session.commit()
            return True

    @staticmethod
    async def update_note(note: "UserNote") -> bool:
        async with async_session_factory() as session:
            q = (
                update(UserNote)
                .where(UserNote.id == note.id)
                .values(dict(text=note.text, title=note.title, file_id=note.file_id))
            )
            await session.execute(q)
            await session.flush()
            await session.commit()
            return True
