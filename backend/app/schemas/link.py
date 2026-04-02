from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List


class LinkBase(BaseModel):
    original_url: str
    custom_alias: Optional[str] = None
    domain: Optional[str] = None
    expires_at: Optional[datetime] = None
    tags: Optional[List[str]] = None


class LinkCreate(LinkBase):
    pass


class LinkUpdate(BaseModel):
    original_url: Optional[str] = None
    custom_alias: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    tags: Optional[List[str]] = None


class LinkResponse(LinkBase):
    id: int
    short_code: str
    is_custom: bool
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class LinkBatchCreate(BaseModel):
    urls: List[str]
    domain: Optional[str] = None
