from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.link import Link
from app.models.stat import LinkStat, DeviceType
from app.schemas.link import LinkResponse
from app.api.stats import parse_user_agent

router = APIRouter(tags=["public"])


@router.get("/{short_code}")
def redirect_to_original(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db)
):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    if not link.is_active:
        raise HTTPException(status_code=410, detail="Link has been deactivated")
    if link.expires_at and link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Link has expired")

    ua_info = parse_user_agent(request.headers.get("user-agent", ""))
    stat = LinkStat(
        link_id=link.id,
        device=ua_info["device"],
        browser=ua_info["browser"],
        os=ua_info["os"],
        referer=request.headers.get("referer")
    )
    db.add(stat)
    db.commit()

    return RedirectResponse(url=link.original_url, status_code=302)


@router.get("/api/info/{short_code}", response_model=LinkResponse)
def get_link_info(
    short_code: str,
    db: Session = Depends(get_db)
):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    if not link.is_active:
        raise HTTPException(status_code=410, detail="Link has been deactivated")
    return link
