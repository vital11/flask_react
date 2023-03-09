from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from sqlalchemy import insert, delete
from sqlalchemy import exc
from psycopg2.errorcodes import FOREIGN_KEY_VIOLATION, UNIQUE_VIOLATION

from app.models.users import User as UserModel
from app.models.groups import Group as GroupModel
from app.models.members import Member as MemberModel
from app.schemas.members import MemberCreate, GroupMember, MemberRoles
from app.exceptions import UniqueError, NotFoundError, NotAuthorizedError


class MemberRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db.session

    def create_member(self, payload: MemberCreate) -> GroupMember:
        stmt = insert(MemberModel).values(
            group_id=payload.group_id,
            user_id=payload.user_id,
            role=MemberRoles.MEMBER
        ).options(
            joinedload(MemberModel.group).load_only(GroupModel.group_name)
        ).options(
            joinedload(MemberModel.member).load_only(UserModel.user_email)
        ).returning(MemberModel)
        try:
            db_member = self.db.scalar(statement=stmt)
            member = GroupMember(
                **db_member.__dict__,
                group_name=db_member.group.group_name,
                user_email=db_member.member.user_email
            )
            self.db.commit()
            return member
        except exc.IntegrityError as err:
            pg_error_code = err.orig.pgcode
            if pg_error_code == UNIQUE_VIOLATION:
                raise UniqueError(f'Member (group_id={payload.group_id}, user_id={payload.user_id}) already registered.')
            if pg_error_code == FOREIGN_KEY_VIOLATION:
                raise NotFoundError(f'Unable to find user or group.')

    def delete_member(self, membership_id: int) -> GroupMember:
        stmt = delete(MemberModel).where(
            MemberModel.membership_id == membership_id
        ).options(
            joinedload(MemberModel.group).load_only(GroupModel.group_name)
        ).options(
            joinedload(MemberModel.member).load_only(UserModel.user_email)
        ).returning(MemberModel)
        try:
            db_member = self.db.scalar(statement=stmt)

            if db_member is None:
                raise NotFoundError(f'Unable to find {membership_id=}.')
            if db_member.role == MemberRoles.OWNER:
                raise NotAuthorizedError(f'Unable to delete group owner from members.')

            member = GroupMember(
                **db_member.__dict__,
                group_name=db_member.group.group_name,
                user_email=db_member.member.user_email
            )
            self.db.commit()
            return member
        except AttributeError:
            raise NotFoundError(f'Unable to find {membership_id=}.')
