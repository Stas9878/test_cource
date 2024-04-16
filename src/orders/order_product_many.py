from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint
from src.database import Base

order_product_many_table = Table(
    'order_product_many',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('order_id', ForeignKey('orders.id'), nullable=False),
    Column('product_id', ForeignKey('products.id'), nullable=False),
    UniqueConstraint('order_id', 'product_id', name='index_unique_order_product')
)