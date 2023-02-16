from flask import Blueprint
from flask_pydantic import validate

from app.schemas.commons import Pagination
from app.schemas.members import MemberCreate, MemberDelete
from app.schemas.users import User

members = Blueprint('members', __name__, url_prefix='/members')


@members.post('/')
@validate()
def add_member(body: MemberCreate) -> User:
    return User(**body.dict())


@members.delete('/')
@validate()
def delete_member(body: MemberDelete) -> User:
    return User(**body.dict())


@members.get('/<group_id>')
@validate(response_many=True)
def reed_members(group_id: int, query: Pagination = None) -> list[User]:
    return [User(member_id=group_id + query.skip + query.limit)]
