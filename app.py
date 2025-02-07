from fastapi import FastAPI, Depends, APIRouter
from xapi_guard_middleware.middleware import XAPIGuardMiddleware
from xapi_guard_middleware.error_codes import APIErrorCode

app = FastAPI(title="XAPI Guard Middleware Example")

guard = XAPIGuardMiddleware(x_api_key="DEN#3xTezZDo1nJg1pO$tIrzQ9A")

# Routers for different route groups
admin_router = APIRouter(dependencies=[Depends(guard.protect)])
settings_router = APIRouter(dependencies=[Depends(guard.protect)])
public_router = APIRouter()

# General routes
@app.get("/", tags=["General"])
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Hello World"}


@app.get("/health", tags=["General"])
async def health():
    """Health check endpoint to verify service status."""
    return {"status": "healthy"}


# Public routes
@public_router.get("/public", tags=["Public"])
async def public():
    """Public endpoint accessible to everyone."""
    return {"message": "This is a public endpoint accessible to everyone."}


# Admin routes
@admin_router.get("/admin", tags=["Admin"])
async def admin():
    """Admin area endpoint."""
    return {"message": "Welcome to the admin area!"}


# Settings routes
@settings_router.get("/settings", tags=["Settings"])
async def settings():
    """Settings page, accessible only to authorized users."""
    return {"message": "Settings page, accessible only to authorized users."}


# Include the routers in the main app
app.include_router(public_router)
app.include_router(admin_router, prefix="/secure")
app.include_router(settings_router, prefix="/secure")
