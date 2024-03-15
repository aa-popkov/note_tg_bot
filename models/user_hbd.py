from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, ForeignKey, String

from . import User
from .base import Base, created_at, updated_at


class UserHappyBirthday(Base):
    person_name: Mapped[str] = mapped_column(String(40))
    person_birthdate: Mapped[datetime]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    user_id: Mapped[str] = mapped_column(ForeignKey(User.tg_id))
