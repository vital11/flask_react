from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from sqlalchemy import desc, select, delete, update
from sqlalchemy import exc
from psycopg2.errorcodes import FOREIGN_KEY_VIOLATION, UNIQUE_VIOLATION
from werkzeug.security import generate_password_hash

from app.models.users import User as UserModel, Contact as ContactModel
from app.models.groups import Group as GroupModel
from app.models.members import Member as MemberModel
from app.schemas.users import User, UserCreate, UserUpdate, Contact, ContactCreate, ContactUpdate, UserContacts
from app.schemas.groups import Group
from app.schemas.commons import Pagination
from app.exceptions import UniqueError, NotFoundError, BadRequestError


class UserRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db.session

    def create_user(self, payload: UserCreate) -> User:
        db_user = UserModel(
            user_email=payload.user_email,
            user_name=payload.user_name,
            hashed_password=generate_password_hash(payload.password)
        )
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return User(**db_user.__dict__)
        except exc.IntegrityError:
            raise UniqueError(f'User with email {payload.user_email} already registered.')

    def reed_user(self, user_id: int) -> User:
        stmt = select(UserModel).where(UserModel.user_id == user_id)
        db_user = self.db.scalar(statement=stmt)
        if db_user is None:
            raise NotFoundError(f'Unable to find user with id {user_id}.')
        return User(**db_user.__dict__)

    def read_users(self, query: Pagination) -> list[User]:
        stmt = (
            select(UserModel)
            .offset(query.skip).limit(query.limit)
            .order_by(desc(UserModel.user_id))
        )
        try:
            db_users = self.db.scalars(statement=stmt)
            return [User(**db_user.__dict__) for db_user in db_users]
        except Exception:
            return []

    def update_user(self, user_id: int, payload: UserUpdate) -> User | None:
        update_data: dict = payload.dict(exclude_unset=True, exclude_none=True)
        if not update_data:
            return None
        if update_data.get('password') is not None:
            hashed_password = generate_password_hash(update_data.get('password'))
            del update_data['password']
            update_data['hashed_password'] = hashed_password
        stmt = (
            update(UserModel)
            .where(UserModel.user_id == user_id)
            .values(**update_data)
            .returning(UserModel)
        )
        db_user = self.db.scalar(statement=stmt)
        user = User(**db_user.__dict__)
        self.db.commit()
        return user

    def delete_user(self, user_id: int) -> User:
        stmt = delete(UserModel).where(UserModel.user_id == user_id).returning(UserModel)
        db_user = self.db.scalar(statement=stmt)
        if db_user is None:
            raise NotFoundError(f'Unable to find user with id {user_id}.')
        user = User(**db_user.__dict__)
        self.db.commit()
        return user

    def add_contacts(self, user_id: int, payload: ContactCreate) -> Contact:
        db_contacts = ContactModel(**payload.dict(), user_id=user_id)
        try:
            self.db.add(db_contacts)
            self.db.commit()
            self.db.refresh(db_contacts)
            return Contact(**db_contacts.__dict__)
        except exc.IntegrityError as err:
            pg_error_code = err.orig.pgcode
            if pg_error_code == UNIQUE_VIOLATION:
                raise UniqueError(f'User id={user_id} contacts already exists.')
            if pg_error_code == FOREIGN_KEY_VIOLATION:
                raise NotFoundError(f'Unable to find user with id {user_id}.')

    def reed_contacts(self, user_id: int) -> UserContacts:
        stmt = (
            select(UserModel)
            .where(UserModel.user_id == user_id)
            .options(joinedload(UserModel.contacts))
        )
        db_user_contacts = self.db.scalar(statement=stmt)
        if db_user_contacts is None:
            raise NotFoundError(f'Unable to find user with id {user_id}.')
        return UserContacts(**db_user_contacts.__dict__)

    def update_contacts(self, user_id: int, payload: ContactUpdate) -> Contact | None:
        update_data: dict = payload.dict(exclude_unset=True, exclude_none=True)
        if not update_data:
            return None
        stmt = (
            update(ContactModel)
            .where(ContactModel.user_id == user_id)
            .values(**update_data)
            .returning(ContactModel)
        )
        try:
            db_contacts = self.db.scalar(statement=stmt)
            contacts = Contact(**db_contacts.__dict__)
            self.db.commit()
            return contacts
        except exc.IntegrityError as e:
            pg_error_code = e.orig.pgcode
            if pg_error_code == UNIQUE_VIOLATION:
                raise UniqueError(f'User id={user_id} contacts already exists.')
            if pg_error_code == FOREIGN_KEY_VIOLATION:
                raise NotFoundError(f'Unable to find user with id {user_id}.')
        except AttributeError:
             raise BadRequestError(f'Unable to find user with id {user_id}.')

    def delete_contacts(self, user_id: int) -> Contact:
        stmt = delete(ContactModel).where(ContactModel.user_id == user_id).returning(ContactModel)
        db_contacts = self.db.scalar(statement=stmt)
        if db_contacts is None:
            raise NotFoundError(f'Unable to find user with id {user_id}.')
        contacts = Contact(**db_contacts.__dict__)
        self.db.commit()
        return contacts

    def read_owner_groups(self, user_id: int, query: Pagination) -> list[Group]:
        stmt = (
            select(GroupModel)
            .where(GroupModel.owner_id == user_id)
            .offset(query.skip).limit(query.limit)
            .order_by(desc(GroupModel.group_id))
        )
        try:
            db_owner_groups = self.db.scalars(statement=stmt)
            return [Group(**db_group.__dict__) for db_group in db_owner_groups]
        except Exception:
            return []

    def read_member_groups(self, user_id: int, query: Pagination) -> list[Group]:
        stmt = (
            select(MemberModel)
            .where(MemberModel.user_id == user_id)
            .offset(query.skip).limit(query.limit)
            .order_by(desc(MemberModel.membership_id))
        )
        try:
            db_member_groups = self.db.scalars(statement=stmt)
            return [Group(**db_group.__dict__) for db_group in db_member_groups]
        except Exception:
            return []
