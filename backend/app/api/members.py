from http import HTTPStatus

from flask import Blueprint, abort
from flask_pydantic import validate

from .dependencies import db
from app.repositories.members import MemberRepository
from app.schemas.members import MemberCreate, GroupMember
from app.exceptions import UniqueError, NotFoundError, NotAuthorizedError


members = Blueprint('members', __name__, url_prefix='/members')


@members.post('/')
@validate()
def add_member(body: MemberCreate) -> GroupMember:
    try:
        member_repo = MemberRepository(db=db)
        return member_repo.create_member(payload=body)
    except UniqueError:
        abort(HTTPStatus.CONFLICT, description='Resource already exist.')
    except NotFoundError:
        abort(HTTPStatus.NOT_FOUND, description='Resource not found.')


@members.delete('/<membership_id>')
@validate()
def remove_member(membership_id: int) -> GroupMember:
    try:
        member_repo = MemberRepository(db=db)
        return member_repo.delete_member(membership_id=membership_id)
    except NotFoundError:
        abort(HTTPStatus.NOT_FOUND, description='Resource not found.')
    except NotAuthorizedError:
        abort(HTTPStatus.FORBIDDEN, description='Resource not found.')
