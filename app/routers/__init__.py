from .servers import router as servers_router
from .applications import router as applications_router
from .installations import router as installations_router

__all__ = ["servers_router", "applications_router", "installations_router"]
