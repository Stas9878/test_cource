from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING
from src.database import Base


if TYPE_CHECKING:
    from src.orders.models import Order
    from src.orders.order_product_many import OrderProductMany


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    orders_details: Mapped[list['OrderProductMany']] = relationship(
        back_populates='product',
    )