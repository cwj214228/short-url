from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import secrets

from app.core.database import get_db
from app.models.user import User
from app.models.domain import Domain
from app.schemas.domain import DomainCreate, DomainResponse, DomainVerify
from app.api.auth import get_current_user

router = APIRouter(prefix="/domains", tags=["domains"])


@router.get("", response_model=List[DomainResponse])
def get_domains(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    domains = db.query(Domain).filter(Domain.user_id == current_user.id).all()
    return domains


@router.post("", response_model=DomainResponse)
def add_domain(
    domain_data: DomainCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Domain).filter(Domain.domain == domain_data.domain).first()
    if existing:
        raise HTTPException(status_code=400, detail="Domain already registered")

    verification_token = secrets.token_urlsafe(32)
    domain = Domain(
        user_id=current_user.id,
        domain=domain_data.domain,
        verification_token=verification_token
    )
    db.add(domain)
    db.commit()
    db.refresh(domain)
    return domain


@router.post("/verify")
def verify_domain(
    verify_data: DomainVerify,
    db: Session = Depends(get_db)
):
    domain = db.query(Domain).filter(Domain.domain == verify_data.domain).first()
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    if domain.verification_token != verify_data.verification_token:
        raise HTTPException(status_code=400, detail="Invalid verification token")

    from datetime import datetime
    domain.verified_at = datetime.utcnow()
    domain.verification_token = None
    db.commit()
    return {"message": "Domain verified successfully"}


@router.delete("/{domain}")
def delete_domain(
    domain: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    domain_obj = db.query(Domain).filter(Domain.domain == domain).first()
    if not domain_obj:
        raise HTTPException(status_code=404, detail="Domain not found")
    if domain_obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(domain_obj)
    db.commit()
    return {"message": "Domain deleted successfully"}