from typing import Union
from fastapi import APIRouter

from schema.Item import Item

router = APIRouter(prefix='/items', tags=['items'])


@router.get('/{id_item}')
async def read_item(id_item: int, q: Union[bool, None] = None):
    return {"item_id": id_item, "is_sell": q}


@router.post("/")
async def create_item(item: Item):
    return {"item": item}


@router.put('/{id_item}')
async def update_item(id_item: int, item: Item):
    return {"id_item": id_item, "item": item}


@router.delete('/{id_item}')
async def delete_item(id_item: int):
    return {"id_item": id_item}
