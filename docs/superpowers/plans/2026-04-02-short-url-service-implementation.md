# Short URL Service Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a public URL shortening service (Bitly-like) with user auth, link management, analytics, and custom domain support.

**Architecture:** Full-stack app with FastAPI backend (Python), Vue 3 + Vite frontend, MySQL database, Redis cache, Nginx reverse proxy.

**Tech Stack:** FastAPI, SQLAlchemy, MySQL, Redis, Vue 3, Vite, TailwindCSS, Pinia, Vue Router

---

## Phase 1: Project Scaffolding

### Task 1: Create Project Directory Structure

**Files:**
- Create: `backend/` (empty directory structure)
- Create: `frontend/` (empty directory structure)
- Create: `nginx/` (empty directory structure)

- [ ] **Step 1: Create base directory structure**

```bash
mkdir -p backend/app/{api,core,models,schemas,services}
mkdir -p frontend/src/{components,views,router,stores,api,assets}
mkdir -p nginx
touch backend/app/__init__.py
touch backend/app/api/__init__.py
touch backend/app/core/__init__.py
touch backend/app/models/__init__.py
touch backend/app/schemas/__init__.py
touch backend/app/services/__init__.py
```

- [ ] **Step 2: Commit**

```bash
git add -A && git commit -m "chore: create project directory structure"
```

---

### Task 2: Backend - Requirements and Dependencies

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/pyproject.toml`

- [ ] **Step 1: Create requirements.txt**

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pymysql==1.1.0
redis==5.0.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.3
pydantic-settings==2.1.0
qrcode==7.4.2
Pillow==10.2.0
httpx==0.26.0
user-agents==2.2.0
geoip2==4.8.0
email-validator==2.1.0
```

- [ ] **Step 2: Commit**

```bash
git add backend/requirements.txt && git commit -m "chore: add backend dependencies"
```

---

### Task 3: Frontend - Package.json and Config

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tailwind.config.js`
- Create: `frontend/postcss.config.js`
- Create: `frontend/tsconfig.json`

- [ ] **Step 1: Create package.json**

```json
{
  "name": "short-url-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.15",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.5",
    "@vueuse/core": "^10.7.2"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.3",
    "typescript": "^5.3.3",
    "vite": "^5.0.11",
    "vue-tsc": "^1.8.27",
    "tailwindcss": "^3.4.1",
    "postcss": "^8.4.33",
    "autoprefixer": "^10.4.17"
  }
}
```

- [ ] **Step 2: Create vite.config.ts**

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

- [ ] **Step 3: Create tailwind.config.js**

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
        secondary: {
          500: '#8B5CF6',
          600: '#7C3AED',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

- [ ] **Step 4: Commit**

```bash
git add frontend/package.json frontend/vite.config.ts frontend/tailwind.config.js frontend/postcss.config.js frontend/tsconfig.json && git commit -m "chore: add frontend project config"
```

---

## Phase 2: Backend Core

### Task 4: Backend Configuration and Database Setup

**Files:**
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/database.py`
- Create: `backend/app/core/security.py`

- [ ] **Step 1: Create config.py**

```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Short URL Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/shorturl"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Short URL
    DEFAULT_DOMAIN: str = "localhost:8000"
    SHORT_CODE_LENGTH: int = 8

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
```

- [ ] **Step 2: Create database.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 3: Create security.py**

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

- [ ] **Step 4: Commit**

```bash
git add backend/app/core/config.py backend/app/core/database.py backend/app/core/security.py && git commit -m "feat: add backend core configuration (config, database, security)"
```

---

### Task 5: Backend Database Models

**Files:**
- Create: `backend/app/models/user.py`
- Create: `backend/app/models/link.py`
- Create: `backend/app/models/stat.py`
- Create: `backend/app/models/domain.py`
- Modify: `backend/app/models/__init__.py`

- [ ] **Step 1: Create user.py**

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class PlanType(str, enum.Enum):
    FREE = "free"
    PRO = "pro"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    plan_type = Column(Enum(PlanType), default=PlanType.FREE)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    links = relationship("Link", back_populates="owner")
    domains = relationship("Domain", back_populates="owner")
```

- [ ] **Step 2: Create link.py**

```python
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # null for anonymous links
    original_url = Column(Text, nullable=False)
    short_code = Column(String(20), unique=True, index=True, nullable=False)
    custom_alias = Column(String(50), unique=True, index=True, nullable=True)
    domain = Column(String(255), default="localhost:8000")
    is_custom = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    tags = Column(JSON, default=list)

    owner = relationship("User", back_populates="links")
    stats = relationship("LinkStat", back_populates="link")
```

- [ ] **Step 3: Create stat.py**

```python
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
```

- [ ] **Step 4: Create domain.py**

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    domain = Column(String(255), unique=True, index=True, nullable=False)
    verification_token = Column(String(100), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="domains")
```

- [ ] **Step 5: Update models/__init__.py**

```python
from app.models.user import User, PlanType
from app.models.link import Link
from app.models.stat import LinkStat, DeviceType
from app.models.domain import Domain

__all__ = ["User", "PlanType", "Link", "LinkStat", "DeviceType", "Domain"]
```

- [ ] **Step 6: Commit**

```bash
git add backend/app/models/ && git commit -m "feat: add database models (User, Link, LinkStat, Domain)"
```

---

### Task 6: Backend Pydantic Schemas

**Files:**
- Create: `backend/app/schemas/user.py`
- Create: `backend/app/schemas/link.py`
- Create: `backend/app/schemas/stat.py`
- Create: `backend/app/schemas/domain.py`
- Create: `backend/app/schemas/token.py`
- Modify: `backend/app/schemas/__init__.py`

- [ ] **Step 1: Create user.py**

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import PlanType


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    plan_type: PlanType
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
```

- [ ] **Step 2: Create token.py**

```python
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int
    type: str
```

- [ ] **Step 3: Create link.py**

```python
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
```

- [ ] **Step 4: Create stat.py**

```python
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
```

- [ ] **Step 5: Create domain.py**

```python
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
```

- [ ] **Step 6: Update schemas/__init__.py**

```python
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.schemas.token import Token, TokenPayload
from app.schemas.link import LinkCreate, LinkUpdate, LinkResponse, LinkBatchCreate
from app.schemas.stat import LinkStatResponse, LinkStatsSummary, TimelinePoint
from app.schemas.domain import DomainCreate, DomainResponse, DomainVerify

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "UserUpdate",
    "Token", "TokenPayload",
    "LinkCreate", "LinkUpdate", "LinkResponse", "LinkBatchCreate",
    "LinkStatResponse", "LinkStatsSummary", "TimelinePoint",
    "DomainCreate", "DomainResponse", "DomainVerify",
]
```

- [ ] **Step 7: Commit**

```bash
git add backend/app/schemas/ && git commit -m "feat: add Pydantic schemas"
```

---

## Phase 3: Backend API Modules

### Task 7: Auth API

**Files:**
- Create: `backend/app/api/auth.py`
- Modify: `backend/app/api/__init__.py`

- [ ] **Step 1: Create auth.py**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=get_password_hash(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    new_access_token = create_access_token(data={"sub": user.id})
    new_refresh_token = create_refresh_token(data={"sub": user.id})
    return Token(access_token=new_access_token, refresh_token=new_refresh_token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

- [ ] **Step 2: Update api/__init__.py**

```python
from app.api.auth import router as auth_router

__all__ = ["auth_router"]
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/api/auth.py && git commit -m "feat: add auth API (register, login, refresh, me)"
```

---

### Task 8: Short Code Generation Service

**Files:**
- Create: `backend/app/services/short_code.py`

- [ ] **Step 1: Create short_code.py**

```python
import hashlib
import random
import string
from sqlalchemy.orm import Session
from app.models.link import Link
from app.core.config import settings


def generate_short_code(original_url: str) -> str:
    """Generate short code using SHA1 hash + collision detection."""
    hash_obj = hashlib.sha1(original_url.encode())
    hash_hex = hash_obj.hexdigest()[:settings.SHORT_CODE_LENGTH]

    return hash_hex


def get_unique_short_code(db: Session, original_url: str, preferred_code: str = None) -> str:
    """Get a unique short code, handling collisions."""
    if preferred_code:
        existing = db.query(Link).filter(Link.short_code == preferred_code).first()
        if not existing:
            return preferred_code

    base_code = generate_short_code(original_url)
    code = base_code

    for attempt in range(3):
        existing = db.query(Link).filter(Link.short_code == code).first()
        if not existing:
            return code
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        code = f"{base_code}-{suffix}"

    raise ValueError("Unable to generate unique short code after 3 attempts")


def validate_custom_alias(alias: str) -> bool:
    """Validate custom alias format."""
    if not alias:
        return False
    if len(alias) < 3 or len(alias) > 50:
        return False
    if not alias.replace('-', '').replace('_', '').isalnum():
        return False
    return True
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/services/short_code.py && git commit -m "feat: add short code generation service"
```

---

### Task 9: Links API

**Files:**
- Create: `backend/app/api/links.py`
- Modify: `backend/app/api/__init__.py`

- [ ] **Step 1: Create links.py**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/api/links.py && git commit -m "feat: add links API (CRUD + batch create)"
```

---

### Task 10: Stats API

**Files:**
- Create: `backend/app/api/stats.py`
- Modify: `backend/app/api/__init__.py`

- [ ] **Step 1: Create stats.py**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/api/stats.py && git commit -m "feat: add stats API (analytics + timeline)"
```

---

### Task 11: Domains API

**Files:**
- Create: `backend/app/api/domains.py`
- Modify: `backend/app/api/__init__.py`

- [ ] **Step 1: Create domains.py**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/api/domains.py && git commit -m "feat: add domains API (CRUD + verification)"
```

---

### Task 12: Public Redirect API

**Files:**
- Create: `backend/app/api/public.py`
- Modify: `backend/app/api/__init__.py`

- [ ] **Step 1: Create public.py**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/api/public.py && git commit -m "feat: add public redirect API"
```

---

### Task 13: Main Application Entry Point

**Files:**
- Create: `backend/app/main.py`

- [ ] **Step 1: Create main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.api.auth import router as auth_router
from app.api.links import router as links_router
from app.api.stats import router as stats_router
from app.api.domains import router as domains_router
from app.api.public import router as public_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(links_router, prefix="/api")
app.include_router(stats_router, prefix="/api")
app.include_router(domains_router, prefix="/api")
app.include_router(public_router)


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/")
def root():
    return {"message": "Short URL Service API", "docs": "/api/docs"}
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/main.py && git commit -m "feat: create FastAPI main application"
```

---

## Phase 4: Frontend Core

### Task 14: Frontend Base Setup

**Files:**
- Create: `frontend/index.html`
- Create: `frontend/src/main.ts`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/assets/main.css`
- Create: `frontend/src/router/index.ts`
- Create: `frontend/src/stores/auth.ts`
- Create: `frontend/src/stores/links.ts`
- Create: `frontend/src/api/axios.ts`

- [ ] **Step 1: Create index.html**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Short URL Service</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

- [ ] **Step 2: Create main.ts**

```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/main.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
```

- [ ] **Step 3: Create App.vue**

```vue
<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <router-view />
  </div>
</template>

<script setup lang="ts">
</script>
```

- [ ] **Step 4: Create main.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply font-sans text-gray-900 dark:text-gray-100;
  }
}

@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-gradient-to-r from-primary-500 to-secondary-500 text-white rounded-lg font-medium transition-transform hover:scale-105;
  }
  .btn-secondary {
    @apply px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg font-medium transition-colors hover:bg-gray-300 dark:hover:bg-gray-600;
  }
  .input-field {
    @apply w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-800;
  }
  .card {
    @apply bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700;
  }
}
```

- [ ] **Step 5: Create router/index.ts**

```typescript
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomePage.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginPage.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterPage.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/links',
      name: 'links',
      component: () => import('@/views/LinksPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/links/new',
      name: 'create-link',
      component: () => import('@/views/CreateLinkPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/links/:shortCode/edit',
      name: 'edit-link',
      component: () => import('@/views/EditLinkPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/links/:shortCode/stats',
      name: 'link-stats',
      component: () => import('@/views/LinkStatsPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/domains',
      name: 'domains',
      component: () => import('@/views/DomainsPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsPage.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
```

- [ ] **Step 6: Create api/axios.ts**

```typescript
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

- [ ] **Step 7: Create stores/auth.ts**

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<any>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(email: string, password: string) {
    const response = await api.post('/auth/login', { email, password })
    token.value = response.data.access_token
    localStorage.setItem('token', response.data.access_token)
    await fetchUser()
  }

  async function register(email: string, username: string, password: string) {
    await api.post('/auth/register', { email, username, password })
    await login(email, password)
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      const response = await api.get('/auth/me')
      user.value = response.data
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  if (token.value) {
    fetchUser()
  }

  return { token, user, isAuthenticated, login, register, logout, fetchUser }
})
```

- [ ] **Step 8: Create stores/links.ts**

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/axios'

export const useLinksStore = defineStore('links', () => {
  const links = ref<any[]>([])
  const currentLink = ref<any>(null)
  const loading = ref(false)

  async function fetchLinks() {
    loading.value = true
    try {
      const response = await api.get('/links')
      links.value = response.data
    } finally {
      loading.value = false
    }
  }

  async function createLink(data: any) {
    const response = await api.post('/links', data)
    return response.data
  }

  async function updateLink(shortCode: string, data: any) {
    const response = await api.put(`/links/${shortCode}`, data)
    return response.data
  }

  async function deleteLink(shortCode: string) {
    await api.delete(`/links/${shortCode}`)
    links.value = links.value.filter(l => l.short_code !== shortCode)
  }

  async function getLink(shortCode: string) {
    const response = await api.get(`/links/${shortCode}`)
    currentLink.value = response.data
    return response.data
  }

  return { links, currentLink, loading, fetchLinks, createLink, updateLink, deleteLink, getLink }
})
```

- [ ] **Step 9: Commit**

```bash
git add frontend/index.html frontend/src/ && git commit -m "feat: add frontend base setup (router, stores, api)"
```

---

### Task 15: Frontend Auth Pages

**Files:**
- Create: `frontend/src/views/LoginPage.vue`
- Create: `frontend/src/views/RegisterPage.vue`
- Create: `frontend/src/components/NavBar.vue`

- [ ] **Step 1: Create LoginPage.vue**

```vue
<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-secondary-500">
    <div class="card p-8 w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6">Welcome Back</h1>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Email</label>
          <input v-model="email" type="email" required class="input-field" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Password</label>
          <input v-model="password" type="password" required class="input-field" />
        </div>
        <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
        <button type="submit" class="btn-primary w-full" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
      <p class="mt-4 text-center text-sm">
        Don't have an account? <router-link to="/register" class="text-primary-500 hover:underline">Sign up</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await authStore.login(email.value, password.value)
    router.push('/dashboard')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
```

- [ ] **Step 2: Create RegisterPage.vue**

```vue
<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-secondary-500">
    <div class="card p-8 w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6">Create Account</h1>
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Email</label>
          <input v-model="email" type="email" required class="input-field" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Username</label>
          <input v-model="username" type="text" required class="input-field" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Password</label>
          <input v-model="password" type="password" required class="input-field" />
        </div>
        <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
        <button type="submit" class="btn-primary w-full" :disabled="loading">
          {{ loading ? 'Creating account...' : 'Sign Up' }}
        </button>
      </form>
      <p class="mt-4 text-center text-sm">
        Already have an account? <router-link to="/login" class="text-primary-500 hover:underline">Sign in</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    await authStore.register(email.value, username.value, password.value)
    router.push('/dashboard')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
```

- [ ] **Step 3: Create NavBar.vue**

```vue
<template>
  <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <router-link to="/" class="text-xl font-bold bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent">
            ShortURL
          </router-link>
          <div v-if="isAuthenticated" class="ml-10 flex space-x-4">
            <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
            <router-link to="/links" class="nav-link">Links</router-link>
            <router-link to="/domains" class="nav-link">Domains</router-link>
          </div>
        </div>
        <div class="flex items-center">
          <template v-if="isAuthenticated">
            <router-link to="/settings" class="nav-link mr-4">Settings</router-link>
            <button @click="handleLogout" class="btn-secondary">Logout</button>
          </template>
          <template v-else>
            <router-link to="/login" class="nav-link">Login</router-link>
            <router-link to="/register" class="btn-primary ml-4">Sign Up</router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

function handleLogout() {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.nav-link {
  @apply px-3 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors;
}
.router-link-active.nav-link {
  @apply text-primary-500;
}
</style>
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/LoginPage.vue frontend/src/views/RegisterPage.vue frontend/src/components/NavBar.vue && git commit -m "feat: add auth pages (login, register, navbar)"
```

---

### Task 16: Home Page and Create Link

**Files:**
- Create: `frontend/src/views/HomePage.vue`
- Create: `frontend/src/views/CreateLinkPage.vue`

- [ ] **Step 1: Create HomePage.vue**

```vue
<template>
  <div>
    <NavBar />
    <div class="max-w-4xl mx-auto py-20 px-4">
      <div class="text-center mb-12">
        <h1 class="text-5xl font-bold mb-4 bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent">
          Shorten Your Links
        </h1>
        <p class="text-xl text-gray-600 dark:text-gray-400">
          Create short, memorable links in seconds
        </p>
      </div>
      <div class="card p-6">
        <form @submit.prevent="handleCreate" class="flex gap-4">
          <input
            v-model="url"
            type="url"
            placeholder="Paste your long URL here..."
            required
            class="input-field flex-1"
          />
          <button type="submit" class="btn-primary whitespace-nowrap" :disabled="loading">
            {{ loading ? 'Creating...' : 'Shorten' }}
          </button>
        </form>
        <div v-if="shortUrl" class="mt-6 p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Your short URL:</p>
          <div class="flex items-center gap-4">
            <input :value="shortUrl" readonly class="input-field flex-1" ref="copyInput" />
            <button @click="copyToClipboard" class="btn-secondary">Copy</button>
          </div>
        </div>
        <div v-if="error" class="mt-4 text-red-500">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import NavBar from '@/components/NavBar.vue'
import api from '@/api/axios'

const url = ref('')
const shortUrl = ref('')
const error = ref('')
const loading = ref(false)
const copyInput = ref<HTMLInputElement | null>(null)

async function handleCreate() {
  loading.value = true
  error.value = ''
  try {
    const response = await api.post('/links', { original_url: url.value })
    shortUrl.value = `${response.data.domain}/${response.data.short_code}`
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to create short URL'
  } finally {
    loading.value = false
  }
}

function copyToClipboard() {
  if (copyInput.value) {
    copyInput.value.select()
    document.execCommand('copy')
  }
}
</script>
```

- [ ] **Step 2: Create CreateLinkPage.vue**

```vue
<template>
  <div>
    <NavBar />
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">Create New Link</h1>
      <div class="card p-6">
        <form @submit.prevent="handleCreate" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Original URL *</label>
            <input v-model="form.original_url" type="url" required class="input-field" placeholder="https://example.com/very/long/url" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Custom Alias (optional)</label>
            <input v-model="form.custom_alias" class="input-field" placeholder="my-custom-link" />
            <p class="text-xs text-gray-500 mt-1">3-50 characters, letters, numbers, hyphens and underscores only</p>
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Tags (optional)</label>
            <input v-model="tagsInput" class="input-field" placeholder="tag1, tag2, tag3" />
          </div>
          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
          <div class="flex gap-4">
            <button type="submit" class="btn-primary" :disabled="loading">
              {{ loading ? 'Creating...' : 'Create Link' }}
            </button>
            <router-link to="/links" class="btn-secondary">Cancel</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { useLinksStore } from '@/stores/links'

const router = useRouter()
const linksStore = useLinksStore()

const form = ref({
  original_url: '',
  custom_alias: ''
})
const tagsInput = ref('')
const error = ref('')
const loading = ref(false)

async function handleCreate() {
  loading.value = true
  error.value = ''
  try {
    const tags = tagsInput.value ? tagsInput.value.split(',').map(t => t.trim()).filter(Boolean) : []
    await linksStore.createLink({ ...form.value, tags })
    router.push('/links')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to create link'
  } finally {
    loading.value = false
  }
}
</script>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/HomePage.vue frontend/src/views/CreateLinkPage.vue && git commit -m "feat: add home page and create link page"
```

---

### Task 17: Links Management Pages

**Files:**
- Create: `frontend/src/views/LinksPage.vue`
- Create: `frontend/src/views/EditLinkPage.vue`

- [ ] **Step 1: Create LinksPage.vue**

```vue
<template>
  <div>
    <NavBar />
    <div class="max-w-7xl mx-auto py-8 px-4">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">My Links</h1>
        <router-link to="/links/new" class="btn-primary">Create New Link</router-link>
      </div>
      <div v-if="loading" class="text-center py-12">Loading...</div>
      <div v-else-if="links.length === 0" class="card p-12 text-center">
        <p class="text-gray-500 mb-4">You haven't created any links yet</p>
        <router-link to="/links/new" class="btn-primary">Create Your First Link</router-link>
      </div>
      <div v-else class="space-y-4">
        <div v-for="link in links" :key="link.id" class="card p-4 flex items-center justify-between">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="font-mono text-primary-500">{{ link.domain }}/{{ link.short_code }}</span>
              <span v-if="link.is_custom" class="text-xs bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400 px-2 py-0.5 rounded">Custom</span>
            </div>
            <p class="text-sm text-gray-500 truncate">{{ link.original_url }}</p>
            <p class="text-xs text-gray-400 mt-1">{{ new Date(link.created_at).toLocaleDateString() }}</p>
          </div>
          <div class="flex items-center gap-2 ml-4">
            <router-link :to="`/links/${link.short_code}/stats`" class="btn-secondary text-sm">Stats</router-link>
            <router-link :to="`/links/${link.short_code}/edit`" class="btn-secondary text-sm">Edit</router-link>
            <button @click="handleDelete(link.short_code)" class="text-red-500 hover:text-red-700 text-sm">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import { useLinksStore } from '@/stores/links'

const linksStore = useLinksStore()
const links = linksStore.links
const loading = linksStore.loading

onMounted(() => {
  linksStore.fetchLinks()
})

async function handleDelete(shortCode: string) {
  if (confirm('Are you sure you want to delete this link?')) {
    await linksStore.deleteLink(shortCode)
  }
}
</script>
```

- [ ] **Step 2: Create EditLinkPage.vue**

```vue
<template>
  <div>
    <NavBar />
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">Edit Link</h1>
      <div v-if="loading" class="text-center py-12">Loading...</div>
      <div v-else-if="!link" class="card p-6 text-center">
        <p class="text-gray-500">Link not found</p>
        <router-link to="/links" class="btn-primary mt-4">Back to Links</router-link>
      </div>
      <div v-else class="card p-6">
        <form @submit.prevent="handleUpdate" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Short URL</label>
            <input :value="`${link.domain}/${link.short_code}`" disabled class="input-field bg-gray-100 dark:bg-gray-700" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Original URL *</label>
            <input v-model="form.original_url" type="url" required class="input-field" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Active</label>
            <label class="flex items-center gap-2">
              <input v-model="form.is_active" type="checkbox" class="w-4 h-4" />
              <span>Link is active</span>
            </label>
          </div>
          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
          <div class="flex gap-4">
            <button type="submit" class="btn-primary" :disabled="loading">Save Changes</button>
            <router-link to="/links" class="btn-secondary">Cancel</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { useLinksStore } from '@/stores/links'

const route = useRoute()
const router = useRouter()
const linksStore = useLinksStore()

const link = ref<any>(null)
const form = ref({
  original_url: '',
  is_active: true
})
const error = ref('')
const loading = ref(false)

onMounted(async () => {
  const shortCode = route.params.shortCode as string
  link.value = await linksStore.getLink(shortCode)
  form.value.original_url = link.value.original_url
  form.value.is_active = link.value.is_active
})

async function handleUpdate() {
  loading.value = true
  error.value = ''
  try {
    await linksStore.updateLink(link.value.short_code, form.value)
    router.push('/links')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to update link'
  } finally {
    loading.value = false
  }
}
</script>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/LinksPage.vue frontend/src/views/EditLinkPage.vue && git commit -m "feat: add links management pages (list, edit)"
```

---

### Task 18: Dashboard and Stats Pages

**Files:**
- Create: `frontend/src/views/DashboardPage.vue`
- Create: `frontend/src/views/LinkStatsPage.vue`

- [ ] **Step 1: Create DashboardPage.vue**

```vue
<template>
  <div>
    <NavBar />
    <div class="max-w-7xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="card p-6">
          <p class="text-sm text-gray-500 mb-1">Total Links</p>
          <p class="text-3xl font-bold text-primary-500">{{ stats.totalLinks }}</p>
        </div>
        <div class="card p-6">
          <p class="text-sm text-gray-500 mb-1">Total Clicks</p>
          <p class="text-3xl font-bold text-secondary-500">{{ stats.totalClicks }}</p>
        </div>
        <div class="card p-6">
          <p class="text-sm text-gray-500 mb-1">Active Links</p>
          <p class="text-3xl font-bold text-green-500">{{ stats.activeLinks }}</p>
        </div>
      </div>
      <div class="card p-6">
        <h2 class="text-lg font-semibold mb-4">Recent Links</h2>
        <div v-if="recentLinks.length === 0" class="text-center text-gray-500 py-8">
          No links yet. <router-link to="/links/new" class="text-primary-500 hover:underline">Create one</router-link>
        </div>
        <div v-else class="space-y-3">
          <div v-for="link in recentLinks" :key="link.id" class="flex items-center justify-between border-b dark:border-gray-700 pb-3">
            <div>
              <span class="font-mono text-primary-500">{{ link.short_code }}</span>
              <p class="text-sm text-gray-500 truncate max-w-md">{{ link.original_url }}</p>
            </div>
            <router-link :to="`/links/${link.short_code}/stats`" class="text-sm text-primary-500 hover:underline">View Stats</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import { useLinksStore } from '@/stores/links'
import api from '@/api/axios'

const linksStore = useLinksStore()
const allStats = ref<any>(null)

const stats = computed(() => ({
  totalLinks: linksStore.links.length,
  totalClicks: allStats.value || 0,
  activeLinks: linksStore.links.filter(l => l.is_active).length
}))

const recentLinks = computed(() => linksStore.links.slice(0, 5))

onMounted(async () => {
  await linksStore.fetchLinks()
  try {
    let total = 0
    for (const link of linksStore.links) {
      const response = await api.get(`/links/${link.short_code}/stats`)
      total += response.data.total_clicks
    }
    allStats.value = total
  } catch {
    allStats.value = 0
  }
})
</script>
```

- [ ] **Step 2: Create LinkStatsPage.vue**

```vue
<template>
  <div>
    <NavBar />
    <div class="max-w-5xl mx-auto py-8 px-4">
      <div class="flex items-center gap-4 mb-6">
        <router-link to="/links" class="text-gray-500 hover:text-gray-700">← Back to Links</router-link>
        <h1 class="text-2xl font-bold">Link Statistics</h1>
      </div>
      <div v-if="loading" class="text-center py-12">Loading...</div>
      <div v-else>
        <div class="card p-6 mb-6">
          <div class="flex items-center gap-4 mb-4">
            <span class="font-mono text-xl text-primary-500">{{ shortCode }}</span>
            <span class="px-2 py-1 text-xs rounded" :class="link?.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
              {{ link?.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
          <p class="text-gray-500 text-sm mb-4">{{ link?.original_url }}</p>
          <p class="text-xs text-gray-400">Created: {{ new Date(link?.created_at).toLocaleString() }}</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="card p-6">
            <p class="text-sm text-gray-500 mb-1">Total Clicks</p>
            <p class="text-3xl font-bold">{{ summary.total_clicks }}</p>
          </div>
          <div class="card p-6">
            <p class="text-sm text-gray-500 mb-1">Unique Clicks</p>
            <p class="text-3xl font-bold">{{ summary.unique_clicks }}</p>
          </div>
          <div class="card p-6">
            <p class="text-sm text-gray-500 mb-1">Top Country</p>
            <p class="text-xl font-bold">{{ topCountry }}</p>
          </div>
          <div class="card p-6">
            <p class="text-sm text-gray-500 mb-1">Top Browser</p>
            <p class="text-xl font-bold">{{ topBrowser }}</p>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="card p-6">
            <h3 class="font-semibold mb-4">By Country</h3>
            <div class="space-y-2">
              <div v-for="(count, country) in summary.by_country" :key="country" class="flex justify-between">
                <span>{{ country }}</span>
                <span class="font-medium">{{ count }}</span>
              </div>
            </div>
          </div>
          <div class="card p-6">
            <h3 class="font-semibold mb-4">By Device</h3>
            <div class="space-y-2">
              <div v-for="(count, device) in summary.by_device" :key="device" class="flex justify-between">
                <span class="capitalize">{{ device }}</span>
                <span class="font-medium">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { useLinksStore } from '@/stores/links'
import api from '@/api/axios'

const route = useRoute()
const linksStore = useLinksStore()

const shortCode = route.params.shortCode as string
const link = ref<any>(null)
const summary = ref({ total_clicks: 0, unique_clicks: 0, by_country: {}, by_device: {}, by_browser: {} })
const loading = ref(false)

const topCountry = computed(() => {
  const countries = summary.value.by_country as Record<string, number>
  return Object.entries(countries).sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A'
})

const topBrowser = computed(() => {
  const browsers = summary.value.by_browser as Record<string, number>
  return Object.entries(browsers).sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A'
})

onMounted(async () => {
  loading.value = true
  try {
    link.value = await linksStore.getLink(shortCode)
    const response = await api.get(`/links/${shortCode}/stats`)
    summary.value = response.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/DashboardPage.vue frontend/src/views/LinkStatsPage.vue && git commit -m "feat: add dashboard and link stats pages"
```

---

### Task 19: Domains and Settings Pages

**Files:**
- Create: `frontend/src/views/DomainsPage.vue`
- Create: `frontend/src/views/SettingsPage.vue`

- [ ] **Step 1: Create DomainsPage.vue**

```vue
<template>
  <div>
    <NavBar />
    <div class="max-w-4xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">Custom Domains</h1>
      <div class="card p-6 mb-6">
        <h2 class="text-lg font-semibold mb-4">Add New Domain</h2>
        <form @submit.prevent="handleAdd" class="flex gap-4">
          <input v-model="newDomain" type="text" required class="input-field flex-1" placeholder="example.com" />
          <button type="submit" class="btn-primary" :disabled="loading">Add Domain</button>
        </form>
        <p class="text-sm text-gray-500 mt-2">
          After adding, you'll need to add a DNS TXT record with the verification token to verify ownership.
        </p>
      </div>
      <div class="card p-6">
        <h2 class="text-lg font-semibold mb-4">Your Domains</h2>
        <div v-if="domains.length === 0" class="text-center text-gray-500 py-8">
          No domains added yet.
        </div>
        <div v-else class="space-y-4">
          <div v-for="domain in domains" :key="domain.id" class="flex items-center justify-between border-b dark:border-gray-700 pb-4">
            <div>
              <span class="font-medium">{{ domain.domain }}</span>
              <span v-if="domain.verified_at" class="ml-2 text-xs text-green-500">Verified</span>
              <span v-else class="ml-2 text-xs text-yellow-500">Pending Verification</span>
              <p v-if="!domain.verified_at" class="text-xs text-gray-400 mt-1">Token: {{ domain.verification_token }}</p>
            </div>
            <button @click="handleDelete(domain.domain)" class="text-red-500 hover:text-red-700">Remove</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import api from '@/api/axios'

const domains = ref<any[]>([])
const newDomain = ref('')
const loading = ref(false)

async function fetchDomains() {
  const response = await api.get('/domains')
  domains.value = response.data
}

async function handleAdd() {
  loading.value = true
  try {
    await api.post('/domains', { domain: newDomain.value })
    newDomain.value = ''
    await fetchDomains()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handleDelete(domain: string) {
  if (confirm(`Delete domain ${domain}?`)) {
    await api.delete(`/domains/${domain}`)
    await fetchDomains()
  }
}

onMounted(fetchDomains)
</script>
```

- [ ] **Step 2: Create SettingsPage.vue**

```vue
<template>
  <div>
    <NavBar />
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">Settings</h1>
      <div class="card p-6 mb-6">
        <h2 class="text-lg font-semibold mb-4">Profile</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Email</label>
            <input v-model="user.email" type="email" disabled class="input-field bg-gray-100 dark:bg-gray-700" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Username</label>
            <input v-model="form.username" type="text" class="input-field" />
          </div>
          <button @click="handleUpdateProfile" class="btn-primary" :disabled="loading">Save Changes</button>
        </div>
      </div>
      <div class="card p-6">
        <h2 class="text-lg font-semibold mb-4">Change Password</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">New Password</label>
            <input v-model="form.password" type="password" class="input-field" />
          </div>
          <div v-if="message" class="text-green-500 text-sm">{{ message }}</div>
          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
          <button @click="handleChangePassword" class="btn-primary" :disabled="loading">Update Password</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const user = ref<any>(null)
const form = reactive({ username: '', password: '' })
const message = ref('')
const error = ref('')
const loading = ref(false)

onMounted(async () => {
  await authStore.fetchUser()
  user.value = authStore.user
  form.username = user.value?.username || ''
})

async function handleUpdateProfile() {
  loading.value = true
  error.value = ''
  try {
    await authStore.updateProfile({ username: form.username })
    message.value = 'Profile updated successfully'
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to update profile'
  } finally {
    loading.value = false
  }
}

async function handleChangePassword() {
  loading.value = true
  error.value = ''
  message.value = ''
  try {
    await authStore.updatePassword({ password: form.password })
    message.value = 'Password updated successfully'
    form.password = ''
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to update password'
  } finally {
    loading.value = false
  }
}
</script>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/DomainsPage.vue frontend/src/views/SettingsPage.vue && git commit -m "feat: add domains and settings pages"
```

---

## Phase 5: Integration & Deployment

### Task 20: Nginx Configuration

**Files:**
- Create: `nginx/nginx.conf`

- [ ] **Step 1: Create nginx.conf**

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server localhost:8000;
    }

    upstream frontend {
        server localhost:3000;
    }

    server {
        listen 80;
        server_name localhost;

        client_max_body_size 10M;

        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

- [ ] **Step 2: Commit**

```bash
git add nginx/nginx.conf && git commit -m "feat: add nginx configuration"
```

---

### Task 21: Docker Compose

**Files:**
- Create: `docker-compose.yml`

- [ ] **Step 1: Create docker-compose.yml**

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: shorturl
      MYSQL_USER: shorturl
      MYSQL_PASSWORD: shorturlpassword
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+pymysql://shorturl:shorturlpassword@db:3306/shorturl
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend
      - frontend

volumes:
  mysql_data:
```

- [ ] **Step 2: Create backend/Dockerfile**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 3: Create frontend/Dockerfile**

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npx", "serve", "dist", "-l", "3000"]
```

- [ ] **Step 4: Commit**

```bash
git add docker-compose.yml backend/Dockerfile frontend/Dockerfile && git commit -m "feat: add Docker configuration"
```

---

## Plan Self-Review

**Spec coverage check:**
- [x] User registration/login - Task 7
- [x] Link CRUD + batch - Task 9
- [x] Stats API - Task 10
- [x] Domain management + verification - Task 11
- [x] Public redirect - Task 12
- [x] Frontend pages (home, auth, links, stats, domains, settings) - Tasks 14-19
- [x] MySQL models - Task 5
- [x] Redis integration - config in Task 4
- [x] Docker/Nginx deployment - Tasks 20-21

**Placeholder scan:**
- All API endpoints defined with exact paths
- All components have implementation code
- No TBD/TODO found

**Type consistency:**
- Schema names match API routes (links, domains, stats)
- Pydantic schemas match database models
- Vue store methods match API calls

---

Plan complete and saved to `docs/superpowers/plans/2026-04-02-short-url-service-implementation.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
