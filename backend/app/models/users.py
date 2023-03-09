from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.groups import Group
from app.models.members import Member


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    user_name: Mapped[Optional[str]] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String(), nullable=False)

    contacts: Mapped['Contact'] = relationship(
        back_populates='user',
        cascade='all, delete'
    )

    owner_groups: Mapped[list['Group']] = relationship(
        back_populates='owner',
        cascade='all, delete',
    )

    member_groups: Mapped[list['Member']] = relationship(
        back_populates='member',
        cascade='all, delete'
    )


class Contact(Base):
    __tablename__ = 'contacts'

    contact_id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(12), unique=True)
    telegram: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    linkedin: Mapped[Optional[str]] = mapped_column(String(50), unique=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    user: Mapped['User'] = relationship(back_populates='contacts')
