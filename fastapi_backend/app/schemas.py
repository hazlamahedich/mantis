import uuid

from fastapi_users import schemas
from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class UserRead(schemas.BaseUser[uuid.UUID]):
    """User schema with tenant information for frontend integration."""
    tenant_id: UUID
    # Note: Full tenant object can be included via relationship if needed
    # tenant: Optional["TenantRead"] = None  # Uncomment if full tenant info is needed

    model_config = {"from_attributes": True}


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class TenantRead(BaseModel):
    """Tenant schema for frontend display."""
    id: UUID
    name: str
    slug: str
    is_active: bool

    model_config = {"from_attributes": True}


# Update UserRead to include full tenant info for dashboard
class UserReadWithTenant(UserRead):
    """Extended user schema with full tenant information."""
    tenant: Optional[TenantRead] = None

    model_config = {"from_attributes": True}


class ItemBase(BaseModel):
    name: str
    description: str | None = None
    quantity: int | None = None


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: UUID
    user_id: UUID
    tenant_id: UUID

    model_config = {"from_attributes": True}
