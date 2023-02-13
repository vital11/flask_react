# Import all the models, so that Base has them before being imported by Alembic

from app.database import Base
from app.models.users import User, Contact
from app.models.groups import Group
from app.models.members import Member
