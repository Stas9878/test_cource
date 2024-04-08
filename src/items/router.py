from fastapi import APIRouter, Path
from typing import Annotated

router = APIRouter(
    prefix='/items',
    tags=['items']
)

@router.get('/')
async def list_items():
    return {
        'item1'
    }


@router.get('/latest/')
async def list_items():
    return {
        'item': {
            'id': '0', 'name': 'latest'
        }
    }

@router.get('/{items_id}/')
async def list_items(items_id: Annotated[int, Path(ge=1, lt=1000000)]):
    return {
        'item': {
            'id': items_id
        }
    }
