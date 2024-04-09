from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from products.schemas import Product, ProductCreate
from db_helper import db_helper
from products import crud

router = APIRouter(
    prefix='/products',
    tags=['Products']
)

@router.get('/', response_model=Product)
async def get_products(session: AsyncSession = Depends(db_helper.session_dependency)) -> list[Product]:
    return await crud.get_products(session=session)


@router.post('/', response_model=Product)
async def create_product(product_in: ProductCreate, session: AsyncSession = Depends(db_helper.session_dependency)) -> Product:
    return await crud.create_product(session=session, product_in=product_in)


@router.get('/{products_id}/', response_model=Product)
async def get_product(product_id: int, session: AsyncSession = Depends(db_helper.session_dependency)) -> Product | None:
    product =  await crud.get_product(product_id=product_id, session=session)
    if product is not None:
        raise product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Products {product_id} not found'
    )