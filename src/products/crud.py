from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from products.schemas import ProductCreate, ProductUpdate, ProductUpdatePartial
from products.models import Product


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return products


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product


async def update_product(session: AsyncSession, product: Product, product_update: ProductUpdate) -> Product:
    for name, val in product.model_dump().items():
        setattr(product, name, val)
    await session.commit()
    return product


async def update_product_partial(session: AsyncSession, product: Product, 
                                 product_update: ProductUpdatePartial | ProductUpdate,
                                 partial: bool=True)  -> Product:
    data = product_update.model_dump(exclude_unset=partial)
    for name, val in data.items():
        setattr(product, name, val)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: Product) -> None:
    await session.delete(product)
