from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.posts.models import Post

class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    posts = Mapped[list['Post']] = relationship('user')

