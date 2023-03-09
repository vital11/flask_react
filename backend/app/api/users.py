from http import HTTPStatus

from flask import Blueprint, abort
from flask_pydantic import validate

from .dependencies import db
from app.repositories.users import UserRepository
from app.exceptions import NotFoundError, UniqueError, BadRequestError
from app.schemas.commons import Pagination
from app.schemas.groups import Group
from app.schemas.users import (User, UserCreate, UserUpdate,
                               Contact, ContactCreate, ContactUpdate, UserContacts)


users = Blueprint('users', __name__, url_prefix='/users')


@users.post('/')
@validate()
def create_user(body: UserCreate) -> User:
    try:
        user_repo = UserRepository(db=db)
        return user_repo.create_user(payload=body)
    except UniqueError:
        abort(HTTPStatus.CONFLICT, description='Resource already exist.')


@users.get('/<user_id>')
@validate()
def reed_user(user_id: int) -> User:
    try:
        user_repo = UserRepository(db=db)
        return user_repo.reed_user(user_id=user_id)
    except NotFoundError:
        abort(HTTPStatus.NOT_FOUND, description='Resource not found.')


@users.get('/')
@validate(response_many=True)
def reed_users(query: Pagination) -> list[User]:
    user_repo = UserRepository(db=db)
    return user_repo.read_users(query=query)


@users.patch('/<user_id>')
@validate()
def update_user(user_id: int, body: UserUpdate) -> User | None:
    user_repo = UserRepository(db=db)
    return user_repo.update_user(user_id=user_id, payload=body)


@users.delete('/<user_id>')
@validate()
def delete_user(user_id: int) -> User:
    try:
        user_repo = UserRepository(db=db)
        return user_repo.delete_user(user_id=user_id)
    except NotFoundError:
        abort(HTTPStatus.NOT_FOUND, description='Resource not found.')


@users.post('/<user_id>/contacts')
@validate()
def add_contacts(user_id: int, body: ContactCreate) -> Contact:
    try:
        user_repo = UserRepository(db=db)
        return user_repo.add_contacts(user_id=user_id, payload=body)
    except UniqueError:
        abort(HTTPStatus.CONFLICT, description='Resource already exist.')
    except NotFoundError:
        abort(HTTPStatus.NOT_FOUND, description='Resource not found.')


@users.get('/<user_id>/contacts')
@validate()
def reed_contacts(user_id: int) -> UserContacts:
    try:
        user_repo = UserRepository(db=db)
        return user_repo.reed_contacts(user_id=user_id)
    except NotFoundError:
        abort(HTTPStatus.NOT_FOUND, description='Resource not found.')


@users.patch('/<user_id>/contacts')
@validate()
def update_contacts(user_id: int, body: ContactUpdate) -> Contact | None:
    try:
        user_repo = UserRepository(db=db)
        return user_repo.update_contacts(user_id=user_id, payload=body)
    except UniqueError:
        abort(HTTPStatus.CONFLICT, description='Resource already exist.')
    except NotFoundError:
        abort(HTTPStatus.NOT_FOUND, description='Resource not found.')
    except BadRequestError:
        abort(HTTPStatus.BAD_REQUEST, description='Resource not found.')


@users.delete('/<user_id>/contacts')
@validate()
def delete_contacts(user_id: int) -> Contact:
    try:
        user_repo = UserRepository(db=db)
        return user_repo.delete_contacts(user_id=user_id)
    except NotFoundError:
        abort(HTTPStatus.NOT_FOUND, description='Resource not found.')


@users.get('/<user_id>/owner')
@validate(response_many=True)
def reed_owner_groups(user_id: int, query: Pagination) -> list[Group]:
    user_repo = UserRepository(db=db)
    return user_repo.read_owner_groups(user_id=user_id, query=query)


@users.get('/<user_id>/member')
@validate(response_many=True)
def reed_member_groups(user_id: int, query: Pagination) -> list[Group]:
    user_repo = UserRepository(db=db)
    return user_repo.read_member_groups(user_id=user_id, query=query)
