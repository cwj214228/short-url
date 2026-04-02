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
