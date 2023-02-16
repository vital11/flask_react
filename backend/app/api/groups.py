from flask import Blueprint
from flask_pydantic import validate

from app.schemas.commons import Pagination
from app.schemas.groups import Group, GroupCreate, GroupUpdate


groups = Blueprint('groups', __name__, url_prefix='/groups')


@groups.post('/')
@validate()
def create_group(body: GroupCreate) -> Group:
    return Group(**body.dict())


@groups.get('/<group_id>')
@validate()
def reed_group(group_id: int) -> Group:
    return Group(group_id=group_id)


@groups.get('/')
@validate(response_many=True)
def reed_groups(query: Pagination = None) -> list[Group]:
    return [Group(group_id=query.skip + query.limit)]


@groups.patch('/<group_id>')
@validate()
def update_group(group_id: int, body: GroupUpdate) -> Group:
    return Group(**body.dict(), group_id=group_id)


@groups.delete('/<group_id>')
@validate()
def delete_group(group_id: int) -> Group:
    return Group(group_id=group_id)
