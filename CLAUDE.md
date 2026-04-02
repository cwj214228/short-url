# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Short URL service (Bitly-like) with FastAPI backend and Vue 3 frontend. Supports public URL shortening, user authentication (JWT), link management, click analytics, custom domains, and QR code generation.

## Commands

### Backend (Python/FastAPI)

```bash
cd backend

# Install dependencies (uses uv)
uv sync

# Run development server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests (none exist yet - tests would go in tests/ directory)
uv run pytest
```

### Frontend (Vue 3/Vite/TypeScript)

```bash
cd frontend

# Install dependencies
npm install

# Run development server (proxies /api to localhost:8000)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Docker (Production)

```bash
docker-compose up -d     # Start all services
docker-compose logs -f   # View logs
docker-compose down      # Stop services
```

Application available at http://localhost:8080

## Architecture

```
User → Nginx (:8080) → Frontend (:3000) or Backend (:8000)
                              ↓
                        MySQL + Redis
```

### Backend Structure (FastAPI)

- `app/main.py` - FastAPI app entry, CORS config, router registration
- `app/api/` - Route handlers (auth, links, stats, domains, public)
- `app/core/config.py` - Settings via pydantic-settings (reads .env)
- `app/core/database.py` - SQLAlchemy setup
- `app/core/security.py` - JWT tokens, bcrypt password hashing (72-byte truncation)
- `app/models/` - SQLAlchemy models (User, Link, Stat, Domain)
- `app/schemas/` - Pydantic schemas for request/response validation
- `app/services/short_code.py` - Short code generation with collision detection

JWT flow: `sub` claim uses `str(user.id)`, parsed with `int(payload.get("sub"))` on decode.

### Frontend Structure (Vue 3)

- `src/api/axios.ts` - Axios instance with JWT interceptor (auto-attaches Bearer token, handles 401 logout)
- `src/stores/` - Pinia stores (auth.ts: login/register/logout/updateProfile/updatePassword, links.ts: link CRUD)
- `src/views/` - Page components (HomePage, LoginPage, RegisterPage, DashboardPage, LinksPage, CreateLinkPage, EditLinkPage, LinkStatsPage, DomainsPage, SettingsPage)
- `src/components/NavBar.vue` - Navigation bar

API base URL: `/api` (proxied to backend in dev, direct in production via Nginx)

### Security Notes

- Passwords hashed with bcrypt, truncated to 72 bytes (bcrypt limitation)
- Access tokens expire in 30 minutes, refresh tokens in 7 days
- 401 responses trigger automatic logout and redirect to /login

## Environment Variables (backend/.env)

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/shorturl
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-super-secret-key
DEBUG=True
DEFAULT_DOMAIN=localhost:8000
SHORT_CODE_LENGTH=8
```

## Key Implementation Details

- Short codes generated via SHA1 hash + collision detection in Redis
- Custom domain verification via DNS TXT record with verification token
- Click tracking: country (GeoIP), device, browser, timestamp
- Frontend uses TailwindCSS with custom primary (indigo) and secondary (violet) color palettes
