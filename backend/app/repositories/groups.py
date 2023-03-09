from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, select, delete, update
from sqlalchemy import exc
from sqlalchemy.orm import joinedload
from psycopg2.errorcodes import FOREIGN_KEY_VIOLATION, UNIQUE_VIOLATION

from app.models.groups import Group as GroupModel
from app.models.members import Member as MemberModel
from app.models.users import User as UserModel
from app.schemas.commons import Pagination
from app.schemas.groups import Group, GroupCreate, GroupUpdate
from app.exceptions import UniqueError, NotFoundError
from app.schemas.members import MemberRoles, GroupMember


class GroupRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db.session

    def create_group(self, payload: GroupCreate) -> Group:
        try:
            db_group = GroupModel(**payload.dict())
            self.db.add(db_group)
            self.db.commit()
            self.db.refresh(db_group)
            group = Group(**db_group.__dict__)

            # Add owner to Member group
            db_member = MemberModel(
                group_id=db_group.group_id,
                user_id=db_group.owner_id,
                role=MemberRoles.OWNER
            )
            self.db.add(db_member)
            self.db.commit()
            return group
        except exc.IntegrityError as err:
            pg_error_code = err.orig.pgcode
            if pg_error_code == UNIQUE_VIOLATION:
                raise UniqueError(f'Group with name "{payload.group_name}" already registered.')
            if pg_error_code == FOREIGN_KEY_VIOLATION:
                raise NotFoundError(f'Unable to find user with id {payload.owner_id}.')

    def reed_group(self, group_id: int) -> Group:
        stmt = select(GroupModel).where(GroupModel.group_id == group_id)
        db_group = self.db.scalar(statement=stmt)
        if db_group is None:
            raise NotFoundError(f'Unable to find group with id {group_id}.')
        return Group(**db_group.__dict__)

    def read_groups(self, query: Pagination) -> list[Group]:
        stmt = (
            select(GroupModel)
            .offset(query.skip).limit(query.limit)
            .order_by(desc(GroupModel.group_id))
        )
        try:
            db_groups = self.db.scalars(statement=stmt)
            return [Group(**db_group.__dict__) for db_group in db_groups]
        except Exception:
            return []

    def update_group(self, group_id: int, payload: GroupUpdate) -> Group | None:
        update_data: dict = payload.dict(exclude_unset=True, exclude_none=True)
        if not update_data:
            return None
        stmt = (
            update(GroupModel)
            .where(GroupModel.group_id == group_id)
            .values(**update_data)
            .returning(GroupModel)
        )
        db_group = self.db.scalar(statement=stmt)
        group = Group(**db_group.__dict__)
        self.db.commit()
        return group

    def delete_group(self, group_id: int) -> Group:
        stmt = delete(GroupModel).where(GroupModel.group_id == group_id).returning(GroupModel)
        db_group = self.db.scalar(statement=stmt)
        if db_group is None:
            raise NotFoundError(f'Unable to find group with id {group_id}.')
        group = Group(**db_group.__dict__)
        self.db.commit()
        return group

    def read_group_members(self, group_id: int, query: Pagination) -> list[GroupMember]:
        stmt = (
            select(MemberModel)
            .where(MemberModel.group_id == group_id)
            .options(joinedload(MemberModel.member).load_only(UserModel.user_email))
            .offset(query.skip).limit(query.limit)
            .order_by(desc(MemberModel.membership_id))
        )
        try:
            db_group_members = self.db.scalars(statement=stmt)
            return [GroupMember(**db_member.__dict__, user_email=db_member.member.user_email)
                    for db_member in db_group_members]
        except Exception:
            return []
