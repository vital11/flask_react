from typing import Optional

from pydantic import BaseModel


class Pagination(BaseModel):
    skip: Optional[int] = None
    limit: Optional[int] = None
