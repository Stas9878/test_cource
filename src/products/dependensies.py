from typing import Annotated
from fastapi import Path, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from products import crud
from products.models import Product
from db_helper import db_helper

async def product_by_id(product_id: Annotated[int, Path], session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> Product:
    product =  await crud.get_product(product_id=product_id, session=session)
    
    if product is not None:
        return product
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Products {product_id} not found'
    )