from flask import Blueprint
from flasgger import swag_from
from flask_pydantic import validate

from app.schemas.commons import Pagination
from app.schemas.groups import Group
from app.schemas.users import (User, UserCreate, UserUpdate,
                               Contact, ContactCreate, ContactUpdate)

users = Blueprint('users', __name__, url_prefix='/users')


@users.post('/')
@swag_from('/app/docs/users/users.yaml')
@validate()
def create_user(body: UserCreate) -> User:
    return User(**body.dict())


@users.get('/<int:user_id>')
@validate()
def reed_user(user_id: int) -> User:
    return User(user_id=user_id)


@users.get('/')
@validate(response_many=True)
def reed_users(query: Pagination = None) -> list[User]:
    return [User(user_id=query.skip + query.limit)]


@users.patch('/<user_id>')
@validate()
def update_user(user_id: int, body: UserUpdate) -> User:
    return User(**body.dict(), user_id=user_id)


@users.delete('/<user_id>')
@validate()
def delete_user(user_id: int) -> User:
    return User(user_id=user_id)


@users.post('/<user_id>/contacts')
@validate()
def add_contacts(body: ContactCreate) -> Contact:
    return Contact(**body.dict())


@users.get('/<user_id>/contacts')
@validate()
def reed_contacts(user_id: int) -> Contact:
    return Contact(user_id=user_id)


@users.patch('/<user_id>/contacts')
@validate()
def update_contacts(user_id: int, body: ContactUpdate) -> Contact:
    return Contact(**body.dict(), user_id=user_id)


@users.delete('/<user_id>/contacts')
@validate()
def delete_contacts(user_id: int) -> Contact:
    return Contact(user_id=user_id)


@users.get('/<user_id>/owner')
@validate(response_many=True)
def reed_user_owner_groups(user_id: int, query: Pagination = None) -> list[Group]:
    return [Group(group_id=user_id + query.skip + query.limit)]


@users.get('/<user_id>/member')
@validate(response_many=True)
def reed_user_member_groups(user_id: int, query: Pagination = None) -> list[Group]:
    return [Group(group_id=user_id + query.skip + query.limit)]
