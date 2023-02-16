from typing import Optional
from pydantic import BaseModel, EmailStr
import enum


class MemberRoles(enum.Enum):
    MEMBER = 'member'
    OWNER = 'owner'


class MemberBase(BaseModel):
    """Shared properties"""
    user_id: Optional[int] = None
    group_id: Optional[int] = None
    role: Optional[MemberRoles] = None


class MemberCreate(MemberBase):
    """Properties to receive via API on creation"""
    user_id: int
    group_id: int
    role: MemberRoles


class MemberDelete(MemberCreate):
    """Properties to receive via API on delete"""
    pass


class MemberInDBBase(MemberBase):
    """Properties shared by models stored in DB"""
    membership_id: Optional[int] = None

    class Config:
        orm_mode = True


class Member(MemberInDBBase):
    """Properties to return via API"""
    pass


class GroupMember(MemberInDBBase):
    """Additional properties to return via API"""
    user_email: Optional[EmailStr]
    group_name: Optional[str]
