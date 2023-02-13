from typing import Optional
from pydantic import BaseModel, constr, validator


class GroupBase(BaseModel):
    """Shared properties"""
    group_name: Optional[str] = None
    group_description: Optional[str] = None
    is_private: Optional[bool] = False
    owner_id: Optional[int]


class GroupCreate(GroupBase):
    """Properties to receive via API on creation"""
    group_name: constr(min_length=1, strip_whitespace=True)
    group_description: constr(min_length=1, strip_whitespace=True)
    owner_id: int


class GroupUpdate(GroupBase):
    """Properties to receive via API on update"""

    @validator('*')
    def empty_str_to_none(cls, value):
        return None if value == '' else value


class GroupInDBBase(GroupBase):
    """Properties shared by models stored in DB"""
    group_id: Optional[int] = None
    owner_id: Optional[int] = None

    class Config:
        orm_mode = True


class Group(GroupInDBBase):
    """Properties to return via API"""
    pass


class GroupInDB(GroupInDBBase):
    """Additional properties stored in DB"""
    pass
