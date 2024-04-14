from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.database import Base
from typing import TYPE_CHECKING


class Profile(Base):
    _user_id_unique: bool = True
    _user_back_populates: str = 'profile'
    
    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] =  mapped_column(String(40))
    bio: Mapped[str | None]

