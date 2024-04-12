from sqlalchemy.orm import Mapped
from src.database import Base

class Product(Base):
    __tablename__ = 'products'

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]