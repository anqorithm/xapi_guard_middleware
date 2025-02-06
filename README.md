# XAPI Guard Middleware

[![PyPI version](https://badge.fury.io/py/xapi-guard-middleware.svg)](https://badge.fury.io/py/xapi-guard-middleware)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/xapi-guard-middleware.svg)](https://pypi.org/project/xapi-guard-middleware/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/xapi-guard-middleware)
![XAPI Guard](https://img.shields.io/badge/XAPI_Guard-0.1.3-blue)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-blue)

XAPI Guard is FastAPI middleware that protects your API endpoints by validating the X-API-Key header. It's designed in a decorator style, so you can annotate your FastAPI endpoints with `@guard.protect` to protect them.

## Features

- Annotate your FastAPI endpoints with `@guard.protect` to protect them
- Protect specific HTTP methods (GET, POST, PUT, DELETE, etc.)
- Exclude paths from protection (e.g. /docs, /openapi.json, etc.)
- Configure API key header name and auto error
- Support for OpenAPI/Swagger documentation (with `@guard.protect` annotation)

## Installation

Choose your preferred installation method:

### Poetry (Recommended)
```bash
poetry add xapi-guard-middleware
```

### Pip
```bash
pip install xapi-guard-middleware
```

## Quick Start

```python
from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from xapi_guard_middleware import XApiKeyMiddleware
from xapi_guard_middleware import XAPIGuard
from http import HTTPMethod

# Create FastAPI app
app = FastAPI(title="XAPI Guard Protected API")

# Your API key
API_KEY = "OuGpk!Qo@Fdet#P^EQ8vGaknVOO"

# API key header configuration
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

# Create guard instance
guard = XAPIGuard(app)

# Add middleware with excluded paths
app.add_middleware(
    XApiKeyMiddleware,
    api_key=API_KEY,
    exclude_paths={  # Public paths
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
    },
)

# Public route
@app.get("/")
async def read_root():
    return {"message": "Hello Protected World!"}

# Public health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Protected route - requires API key
@guard.protect("/protected", method=HTTPMethod.POST)
async def protected_route():
    return {"message": "This is a protected route"}
```

## Usage Examples

### Protecting Specific HTTP Methods

```python
# Protect only POST requests
@guard.protect("/users", method=HTTPMethod.POST)
async def create_user():
    return {"message": "User created"}

# Protect specific method
@guard.protect("/admin", method=HTTPMethod.GET)
async def admin_route():
    return {"message": "Admin access"}
```

### Making Requests

```bash
# Unauthorized request (missing API key)
curl -X POST http://localhost:8000/protected
# Response: {"detail": "X-API-Key header missing"}
# Status code: 401

# Unauthorized request (invalid API key)
curl -X POST http://localhost:8000/protected -H "X-API-Key: wrong-key"
# Response: {"detail": "Invalid X-API-Key"}
# Status code: 403

# Authorized request
curl -X POST http://localhost:8000/protected -H "X-API-Key: YOUR_API_KEY"
# Response: {"message": "This is a protected route"}
# Status code: 200
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
## Contributors

- [Abdullah Alqahtani](https://github.com/anqorithm)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
