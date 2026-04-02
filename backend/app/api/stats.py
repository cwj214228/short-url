from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional, List
import user_agents

from app.core.database import get_db
from app.models.link import Link
from app.models.stat import LinkStat, DeviceType
from app.models.user import User
from app.schemas.stat import LinkStatsSummary, TimelinePoint, LinkStatResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/links", tags=["stats"])


def parse_user_agent(user_agent_str: str) -> dict:
    """Parse user agent string into components."""
    if not user_agent_str:
        return {"device": DeviceType.DESKTOP, "browser": "Unknown", "os": "Unknown"}
    ua = user_agents.parse(user_agent_str)
    if ua.is_mobile:
        device = DeviceType.MOBILE
    elif ua.is_tablet:
        device = DeviceType.TABLET
    else:
        device = DeviceType.DESKTOP
    return {
        "device": device,
        "browser": ua.browser.family or "Unknown",
        "os": ua.os.family or "Unknown"
    }


def record_click(db: Session, link_id: int, request_data: dict = None):
    """Record a click event."""
    ua_info = parse_user_agent(request_data.get("user_agent", "") if request_data else "")
    stat = LinkStat(
        link_id=link_id,
        country=request_data.get("country") if request_data else None,
        city=request_data.get("city") if request_data else None,
        device=ua_info["device"],
        browser=ua_info["browser"],
        os=ua_info["os"],
        referer=request_data.get("referer") if request_data else None
    )
    db.add(stat)
    db.commit()


@router.get("/{short_code}/stats", response_model=LinkStatsSummary)
def get_link_stats(
    short_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    if link.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    stats = db.query(LinkStat).filter(LinkStat.link_id == link.id).all()

    total_clicks = len(stats)
    unique_clicks = len(set(s.country for s in stats if s.country))

    by_country = {}
    by_device = {d.value: 0 for d in DeviceType}
    by_browser = {}

    for s in stats:
        if s.country:
            by_country[s.country] = by_country.get(s.country, 0) + 1
        by_device[s.device.value] = by_device.get(s.device.value, 0) + 1
        if s.browser:
            by_browser[s.browser] = by_browser.get(s.browser, 0) + 1

    return LinkStatsSummary(
        total_clicks=total_clicks,
        unique_clicks=unique_clicks,
        by_country=by_country,
        by_device=by_device,
        by_browser=by_browser
    )


@router.get("/{short_code}/stats/timeline", response_model=List[TimelinePoint])
def get_link_stats_timeline(
    short_code: str,
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    if link.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    start_date = datetime.utcnow() - timedelta(days=days)

    results = (
        db.query(
            func.date(LinkStat.clicked_at).label("date"),
            func.count(LinkStat.id).label("clicks")
        )
        .filter(LinkStat.link_id == link.id, LinkStat.clicked_at >= start_date)
        .group_by(func.date(LinkStat.clicked_at))
        .all()
    )

    timeline = [TimelinePoint(date=str(r.date), clicks=r.clicks) for r in results]
    return timeline
