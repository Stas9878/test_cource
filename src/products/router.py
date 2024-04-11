from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from products.schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from products.dependensies import product_by_id
from db_helper import db_helper
from products import crud

router = APIRouter(
    prefix='/products',
    tags=['Products']
)


@router.get('/', response_model=Product, status_code=status.HTTP_201_CREATED)
async def get_products(session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> list[Product]:
    return await crud.get_products(session=session)


@router.post('/', response_model=Product)
async def create_product(product_in: ProductCreate, session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> Product:
    return await crud.create_product(session=session, product_in=product_in)


@router.get('/{product_id}/', response_model=Product)
async def get_product(product: Product = Depends(product_by_id)) -> Product | None:
    return product
    
    
@router.put('/{product_id}/')
async def update_product(product_update: ProductUpdate,
                        product: Product = Depends(product_by_id),
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update
    )

@router.patch('/{product_id}/')
async def update_product(product_update: ProductUpdatePartial,
                        product: Product = Depends(product_by_id),
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.update_product_partial(
        session=session,
        product=product,
        product_update=product_update,
        partial=True
    )


@router.delete('/product_id/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product: Product = Depends(product_by_id),
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> None:
    await crud.delete_product(
        session=session,
        product=product
    )