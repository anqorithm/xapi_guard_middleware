# XAPI Guard

# TL;DR

## Description

XAPI Guard is a FastAPI middleware that protects your API endpoints by validating API keys.

## Installation

```bash
poetry install xapi-guard
```

## Usage

```python
from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from xapi_guard import XApiKeyMiddleware
from xapi_guard import XAPIGuard
from http import HTTPMethod

app = FastAPI(title="XAPI Guard Protected API")

API_KEY = "OuGpk!Qo@Fdet#P^EQ8vGaknVOO"

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

guard = XAPIGuard(app)

app.add_middleware(
    XApiKeyMiddleware,
    api_key=API_KEY,
    exclude_paths={
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
    },
)

@app.get("/")
async def read_root():
    return {"message": "Hello Protected World!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@guard.protect("/protected", method=HTTPMethod.POST)
async def protected_route():
    return {"message": "This is a protected route"}
```