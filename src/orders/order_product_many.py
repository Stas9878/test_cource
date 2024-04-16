from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from src.database import Base


if TYPE_CHECKING:
    from src.orders.models import Order
    from src.products.models import Product


class OrderProductMany(Base):
    __tablename__ = 'order_product_many'
    __table_args__ = (
        UniqueConstraint(
            'order_id', 
            'product_id', 
            name='index_unique_order_product'),
        {'extend_existing': True} 
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    count: Mapped[int] = mapped_column(default=1, server_default='1')
    unit_price: Mapped[int] = mapped_column(default=0, server_default='0')

    child: Mapped['Order'] = relationship(back_populates='products_details')
    parent: Mapped['Product'] = relationship(back_populates='orders_details')