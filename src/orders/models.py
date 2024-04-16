from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from datetime import datetime
from typing import TYPE_CHECKING
from src.database import Base
from src.orders.order_product_many import OrderProductMany


if TYPE_CHECKING:
    from src.products.models import Product


class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now
    )
    # products: Mapped[list['Product']] = relationship(
    #     secondary='order_product_many',
    #     back_populates='orders',
    # )
    
    products_details: Mapped[list['OrderProductMany']] = relationship(
        back_populates='order',
    )