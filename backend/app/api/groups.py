from http import HTTPStatus

from flask import Blueprint, abort
from flask_pydantic import validate

from .dependencies import db
from app.repositories.groups import GroupRepository
from app.schemas.groups import Group, GroupCreate, GroupUpdate
from app.schemas.members import GroupMember
from app.schemas.commons import Pagination
from app.exceptions import UniqueError, NotFoundError


groups = Blueprint('groups', __name__, url_prefix='/groups')


@groups.post('/')
@validate()
def create_group(body: GroupCreate) -> Group:
    try:
        group_repo = GroupRepository(db=db)
        return group_repo.create_group(payload=body)
    except UniqueError:
        abort(HTTPStatus.CONFLICT, description='Resource already exist.')
    except NotFoundError:
        abort(HTTPStatus.NOT_FOUND, description='Resource not found.')


@groups.get('/<group_id>')
@validate()
def reed_group(group_id: int) -> Group:
    try:
        group_repo = GroupRepository(db=db)
        return group_repo.reed_group(group_id=group_id)
    except NotFoundError:
        abort(HTTPStatus.NOT_FOUND, description='Resource not found.')


@groups.get('/')
@validate(response_many=True)
def reed_groups(query: Pagination) -> list[Group]:
    group_repo = GroupRepository(db=db)
    return group_repo.read_groups(query=query)


@groups.patch('/<group_id>')
@validate()
def update_group(group_id: int, body: GroupUpdate) -> Group | None:
    group_repo = GroupRepository(db=db)
    return group_repo.update_group(group_id=group_id, payload=body)


@groups.delete('/<group_id>')
@validate()
def delete_group(group_id: int) -> Group:
    try:
        group_repo = GroupRepository(db=db)
        return group_repo.delete_group(group_id=group_id)
    except NotFoundError:
        abort(HTTPStatus.NOT_FOUND, description='Resource not found.')


@groups.get('/<group_id>/members')
@validate(response_many=True)
def reed_group_members(group_id: int, query: Pagination = None) -> list[GroupMember]:
    group_repo = GroupRepository(db=db)
    return group_repo.read_group_members(group_id=group_id, query=query)
