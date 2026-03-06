from pydantic import BaseModel
from typing import Optional, List

# ---------------------------
# Base schema (common fields)
# ---------------------------
class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


# --------------------------
# Schema for create category
# --------------------------
class CategoryCreate(CategoryBase):
    pass


# --------------------------
# Schema for update category
# --------------------------
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


# ------------------------------------------------
# Response schema (shows nested children)
# ------------------------------------------------
class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    children: List["CategoryResponse"] = []   # nested categories

    class Config:
        orm_mode = True


# forward reference (required for self-nested model)
CategoryResponse.update_forward_refs()
