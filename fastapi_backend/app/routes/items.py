from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.future import select

from app.core.deps import SessionDep, get_current_user
from app.models import User, Item
from app.schemas import ItemRead, ItemCreate

router = APIRouter(tags=["item"])


def transform_items(items: Any) -> list[ItemRead]:
    return [ItemRead.model_validate(item) for item in items]


@router.get("/", response_model=Page[ItemRead])
async def read_item(
    session: SessionDep,
    user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
) -> Page[ItemRead]:
    params = Params(page=page, size=size)
    query = select(Item).filter(Item.user_id == user.id)
    return await apaginate(session, query, params, transformer=transform_items)


@router.post("/", response_model=ItemRead)
async def create_item(
    item: ItemCreate,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> ItemRead:
    db_item = Item(**item.model_dump(), user_id=user.id)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
async def delete_item(
    item_id: UUID,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> dict[str, str]:
    result = await session.execute(
        select(Item).filter(Item.id == item_id, Item.user_id == user.id)
    )
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not authorized")

    await session.delete(item)
    await session.commit()

    return {"message": "Item successfully deleted"}
