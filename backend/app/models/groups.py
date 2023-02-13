from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Group(Base):
    __tablename__ = 'groups'

    group_id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    group_description: Mapped[Optional[str]] = mapped_column(String(500))
    is_private: Mapped[bool] = mapped_column(default=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    owner: Mapped['User'] = relationship(back_populates='owner_groups')

    members: Mapped[list['Member']] = relationship(
        back_populates='group',
        cascade='all, delete'
    )
