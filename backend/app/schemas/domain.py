from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DomainBase(BaseModel):
    domain: str


class DomainCreate(DomainBase):
    pass


class DomainResponse(DomainBase):
    id: int
    user_id: int
    is_active: bool
    verified_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class DomainVerify(BaseModel):
    domain: str
    verification_token: str
