from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from xapi_guard_middleware import XApiKeyMiddleware, XAPIGuard
from http import HTTPMethod

app = FastAPI(title="XAPI Guard Middleware Protected API")

API_KEY = "OuGpk!Qo@Fdet#P^EQ8vGaknVOO"

guard = XAPIGuard(app)

app.add_middleware(
    XApiKeyMiddleware,
    api_key=API_KEY,
    exclude_paths={
        "/",
        "/docs",
        "/health",
        "/redoc",
        "/favicon.ico",
        "/openapi.json",
    },
)

@app.get("/")
async def read_root():
    return {"message": "Hello World!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@guard.protect("/protected", method=HTTPMethod.POST)
async def protected_route():
    return {"message": "This is a protected route"}
