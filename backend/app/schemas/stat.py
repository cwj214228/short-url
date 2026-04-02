from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.stat import DeviceType


class LinkStatBase(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    device: DeviceType = DeviceType.DESKTOP
    browser: Optional[str] = None
    os: Optional[str] = None
    referer: Optional[str] = None


class LinkStatResponse(LinkStatBase):
    id: int
    link_id: int
    clicked_at: datetime

    class Config:
        from_attributes = True


class LinkStatsSummary(BaseModel):
    total_clicks: int
    unique_clicks: int
    by_country: dict
    by_device: dict
    by_browser: dict


class TimelinePoint(BaseModel):
    date: str
    clicks: int
