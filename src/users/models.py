from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.post import Post
    from src.models.profile import Profile

class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    posts: Mapped[list['Post']] = relationship(back_populates='user')
    profile: Mapped['Profile'] = relationship(back_populates='user')

