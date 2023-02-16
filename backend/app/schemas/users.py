from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator


class ContactBase(BaseModel):
    """Shared properties"""
    user_id: Optional[int] = None
    phone_number: Optional[str] = None
    telegram: Optional[str] = None
    linkedin: Optional[str] = None


class ContactCreate(ContactBase):
    """Properties to receive via API on creation"""
    user_id: int


class ContactUpdate(ContactCreate):
    """Properties to receive via API on update"""
    phone_number: Optional[constr(strip_whitespace=True)] = None
    telegram: Optional[constr(strip_whitespace=True)] = None
    linkedin: Optional[constr(strip_whitespace=True)] = None

    @validator('*')
    def empty_str_to_none(cls, value):
        return None if value == '' else value


class ContactInDBBase(ContactBase):
    """Properties shared by models stored in DB"""
    contact_id: Optional[int] = None

    class Config:
        orm_mode = True


class Contact(ContactInDBBase):
    """Properties to return via API"""
    pass


class ContactInDB(ContactInDBBase):
    """Additional properties stored in DB"""
    pass


class UserBase(BaseModel):
    """Shared properties"""
    user_email: Optional[EmailStr] = None
    user_name: Optional[str] = None


class UserCreate(UserBase):
    """Properties to receive via API on creation"""
    user_email: EmailStr
    password: constr(min_length=1, strip_whitespace=True)


class UserUpdate(BaseModel):
    """Properties to receive via API on update"""
    user_name: Optional[constr(strip_whitespace=True)] = None
    password: Optional[constr(strip_whitespace=True)] = None

    @validator('*')
    def empty_str_to_none(cls, value):
        return None if value == '' else value


class UserInDBBase(UserBase):
    """Properties shared by models stored in DB"""
    user_id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    """Properties to return via API"""
    contacts: Optional[Contact] = None


class UserInDB(UserInDBBase):
    """Additional properties stored in DB"""
    hashed_password: str

