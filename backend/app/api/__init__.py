from app.api.auth import router as auth_router
from app.api.links import router as links_router
from app.api.stats import router as stats_router
from app.api.domains import router as domains_router

__all__ = ["auth_router", "links_router", "stats_router", "domains_router"]
