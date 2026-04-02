# Short URL Service

A public URL shortening service similar to Bitly/TinyURL, built with FastAPI and Vue 3.

## Features

- **Public URL shortening** - Anyone can create short links without an account
- **User authentication** - Register/login with JWT tokens
- **Link management** - Create, edit, delete, and batch create links
- **Custom aliases** - Create branded short URLs with custom aliases
- **Click analytics** - Track clicks by country, device, browser, and timeline
- **Custom domains** - Users can bind their own domains
- **QR code generation** - Generate QR codes for links

## Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | FastAPI (Python 3.11) |
| Frontend | Vue 3 + Vite + TypeScript |
| Database | MySQL 8.0 |
| Cache | Redis |
| UI | TailwindCSS |
| State | Pinia |
| Router | Vue Router |
| Proxy | Nginx |
| Container | Docker |

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  User (Browser)                  │
└─────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────┐
│                      Nginx                        │
│            (Reverse Proxy, Port 8080)            │
└─────────────────────────────────────────────────┘
          │                        │
          ▼                        ▼
┌──────────────────┐    ┌──────────────────┐
│     Frontend     │    │      Backend      │
│   (Vue 3, :3000) │    │  (FastAPI, :8000) │
└──────────────────┘    └──────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
            ┌──────────────┐        ┌──────────────┐
            │     MySQL    │        │     Redis    │
            │   (Port 3306) │        │  (Port 6379) │
            └──────────────┘        └──────────────┘
```

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (modern Python package manager)
- Node.js 20+
- MySQL 8.0
- Redis 7+
- Docker & Docker Compose (optional)

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=mysql+pymysql://shorturl:shorturlpassword@localhost:3306/shorturl

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT (change this in production!)
SECRET_KEY=your-super-secret-key-change-in-production

# Application
DEBUG=True
DEFAULT_DOMAIN=localhost:8000
SHORT_CODE_LENGTH=8
```

## Installation

### Option 1: Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The application will be available at:
- Frontend: http://localhost:8080
- Backend API: http://localhost:8080/api
- API Docs: http://localhost:8080/api/docs

### Option 2: Manual Installation

#### Backend

```bash
cd backend

# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# Or if you prefer manual approach:
# uv venv
# uv pip install -r requirements.txt

# Create MySQL database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS shorturl CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p -e "CREATE USER IF NOT EXISTS 'shorturl'@'localhost' IDENTIFIED BY 'shorturlpassword';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON shorturl.* TO 'shorturl'@'localhost';"
mysql -u root -p -e "FLUSH PRIVILEGES;"

# Start Redis (ensure it's running)
redis-server

# Run the application
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at http://localhost:3000 and proxies API requests to http://localhost:8000.

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Key Endpoints

#### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get tokens |
| POST | `/api/auth/refresh` | Refresh access token |
| GET | `/api/auth/me` | Get current user info |

#### Links
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/links` | Create short link |
| GET | `/api/links` | List user's links |
| GET | `/api/links/{code}` | Get link details |
| PUT | `/api/links/{code}` | Update link |
| DELETE | `/api/links/{code}` | Delete link |
| POST | `/api/links/batch` | Batch create links |

#### Statistics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/links/{code}/stats` | Get link statistics |
| GET | `/api/links/{code}/stats/timeline` | Get click timeline |

#### Domains
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/domains` | List user's domains |
| POST | `/api/domains` | Add new domain |
| POST | `/api/domains/verify` | Verify domain ownership |
| DELETE | `/api/domains/{domain}` | Remove domain |

#### Public
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/{short_code}` | Redirect to original URL |
| GET | `/api/info/{code}` | Get link info (public) |

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/            # API route handlers
│   │   │   ├── auth.py     # Authentication endpoints
│   │   │   ├── links.py    # Link CRUD endpoints
│   │   │   ├── stats.py    # Statistics endpoints
│   │   │   ├── domains.py  # Domain management
│   │   │   └── public.py   # Public redirect handler
│   │   ├── core/           # Core configuration
│   │   │   ├── config.py   # Settings and environment
│   │   │   ├── database.py # SQLAlchemy setup
│   │   │   └── security.py # JWT and password utilities
│   │   ├── models/         # Database models
│   │   │   ├── user.py     # User model
│   │   │   ├── link.py     # Link model
│   │   │   ├── stat.py     # Click statistics model
│   │   │   └── domain.py   # Custom domain model
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   │   └── short_code.py # Short code generation
│   │   └── main.py         # FastAPI application entry
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/            # Axios API client
│   │   ├── components/     # Vue components
│   │   │   └── NavBar.vue
│   │   ├── router/         # Vue Router config
│   │   ├── stores/         # Pinia state stores
│   │   │   ├── auth.ts     # Auth state
│   │   │   └── links.ts    # Links state
│   │   ├── views/          # Page components
│   │   │   ├── HomePage.vue
│   │   │   ├── LoginPage.vue
│   │   │   ├── RegisterPage.vue
│   │   │   ├── DashboardPage.vue
│   │   │   ├── LinksPage.vue
│   │   │   ├── CreateLinkPage.vue
│   │   │   ├── EditLinkPage.vue
│   │   │   ├── LinkStatsPage.vue
│   │   │   ├── DomainsPage.vue
│   │   │   └── SettingsPage.vue
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── assets/
│   │       └── main.css
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── nginx/
│   └── nginx.conf           # Nginx configuration
│
├── docker-compose.yml       # Docker orchestration
└── README.md
```

## Development

### Running Tests

Backend tests:
```bash
cd backend
uv run pytest
```

Frontend (if tests are added):
```bash
cd frontend
npm test
```

### Code Quality

Backend linting:
```bash
cd backend
ruff check .
black .
```

Frontend linting:
```bash
cd frontend
npm run lint
```

## Deployment

### Docker Production Deployment

1. Clone the repository
2. Update `SECRET_KEY` in backend `.env`
3. Update domain names in `nginx/nginx.conf`
4. Update CORS settings in `backend/app/main.py`
5. Run `docker-compose -f docker-compose.yml up -d`

### Manual Production Deployment

1. Build frontend: `cd frontend && npm run build`
2. Serve `frontend/dist/` with Nginx
3. Run backend with Gunicorn/Uvicorn
4. Configure Nginx to proxy API and static files

## License

MIT
