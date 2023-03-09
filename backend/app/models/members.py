from sqlalchemy import ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.schemas.members import MemberRoles


class Member(Base):
    """Association Table"""
    __tablename__ = 'members'

    membership_id: Mapped[int] = mapped_column(primary_key=True)

    group_id: Mapped[int] = mapped_column(ForeignKey('groups.group_id', ondelete='CASCADE', onupdate='CASCADE'))
    group: Mapped['Group'] = relationship(back_populates='members')

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'))
    member: Mapped['User'] = relationship(back_populates='member_groups')

    role: Mapped[Enum] = mapped_column(Enum(MemberRoles), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'group_id', name='uniq_member'),
    )
