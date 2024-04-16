from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from src.database import Base
from datetime import datetime

class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now
    )