from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class DeviceType(str, enum.Enum):
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"


class LinkStat(Base):
    __tablename__ = "link_stats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    link_id = Column(Integer, ForeignKey("links.id"), nullable=False)
    clicked_at = Column(DateTime, default=datetime.utcnow, index=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    device = Column(Enum(DeviceType), default=DeviceType.DESKTOP)
    browser = Column(String(100), nullable=True)
    os = Column(String(100), nullable=True)
    referer = Column(Text, nullable=True)

    link = relationship("Link", back_populates="stats")
