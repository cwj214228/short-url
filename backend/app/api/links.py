from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.models.link import Link
from app.schemas.link import LinkCreate, LinkUpdate, LinkResponse, LinkBatchCreate
from app.api.auth import get_current_user
from app.services.short_code import get_unique_short_code, validate_custom_alias

router = APIRouter(prefix="/links", tags=["links"])


@router.post("", response_model=LinkResponse)
def create_link(
    link_data: LinkCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    custom_alias = link_data.custom_alias
    if custom_alias:
        if not validate_custom_alias(custom_alias):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid custom alias format")
        existing = db.query(Link).filter(Link.custom_alias == custom_alias).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Custom alias already taken")

    short_code = get_unique_short_code(db, link_data.original_url, custom_alias)

    link = Link(
        user_id=current_user.id if current_user else None,
        original_url=link_data.original_url,
        short_code=short_code,
        custom_alias=custom_alias if custom_alias else None,
        domain=link_data.domain or settings.DEFAULT_DOMAIN,
        is_custom=bool(custom_alias),
        expires_at=link_data.expires_at,
        tags=link_data.tags or []
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.post("/batch", response_model=List[LinkResponse])
def create_batch_links(
    batch_data: LinkBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    links = []
    for url in batch_data.urls[:100]:
        short_code = get_unique_short_code(db, url)
        link = Link(
            user_id=current_user.id,
            original_url=url,
            short_code=short_code,
            domain=batch_data.domain or settings.DEFAULT_DOMAIN
        )
        db.add(link)
        links.append(link)
    db.commit()
    for link in links:
        db.refresh(link)
    return links


@router.get("", response_model=List[LinkResponse])
def get_links(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    links = db.query(Link).filter(Link.user_id == current_user.id).offset(skip).limit(limit).all()
    return links


@router.get("/{short_code}", response_model=LinkResponse)
def get_link(
    short_code: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    if link.user_id and link.user_id != (current_user.id if current_user else None):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return link


@router.put("/{short_code}", response_model=LinkResponse)
def update_link(
    short_code: str,
    link_data: LinkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    if link.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    if link_data.custom_alias is not None:
        if link_data.custom_alias and validate_custom_alias(link_data.custom_alias):
            existing = db.query(Link).filter(Link.custom_alias == link_data.custom_alias, Link.id != link.id).first()
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Custom alias already taken")
            link.custom_alias = link_data.custom_alias
            link.is_custom = True

    if link_data.original_url:
        link.original_url = link_data.original_url
    if link_data.expires_at is not None:
        link.expires_at = link_data.expires_at
    if link_data.is_active is not None:
        link.is_active = link_data.is_active
    if link_data.tags is not None:
        link.tags = link_data.tags

    db.commit()
    db.refresh(link)
    return link


@router.delete("/{short_code}")
def delete_link(
    short_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    if link.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    db.delete(link)
    db.commit()
    return {"message": "Link deleted successfully"}
