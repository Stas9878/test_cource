from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from src.database import Base
from typing import TYPE_CHECKING
from src.models.mixins import UserRelationMixin


if TYPE_CHECKING:
    from src.users.models import User

class Post(UserRelationMixin, Base):
    _user_back_populates = 'posts'

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default='',
        server_default=''
    )

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id}, title={self.title!r}, user_id={self.user.username})'

    def __repr__(self) -> str:
        return str(self)
