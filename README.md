# XAPI Guard Middleware

[![Downloads](https://img.shields.io/pypi/dm/xapi-guard-middleware)](https://pypi.org/project/xapi-guard-middleware/)
[![PyPI version](https://badge.fury.io/py/xapi-guard-middleware.svg)](https://badge.fury.io/py/xapi-guard-middleware)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![XAPI Guard](https://img.shields.io/badge/XAPI_Guard-0.1.6-blue)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

XAPI Guard is FastAPI middleware that protects your API endpoints by validating the X-API-Key header. It's designed in a decorator style, so you can annotate your FastAPI endpoints with `@guard.protect` to protect them.

## Features

- Protect your FastAPI endpoints by validating the `X-API-Key` header.
- Use `@guard.protect` to secure specific routes or entire routers.
- Easily configure which routes require protection and which are public.
- Automatically handle unauthorized access with appropriate error messages.
- Support for OpenAPI/Swagger documentation with protected routes.

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
from fastapi import FastAPI, Depends, APIRouter
from xapi_guard_middleware.middleware import XAPIGuardMiddleware

app = FastAPI(title="XAPI Guard Middleware Example")

guard = XAPIGuardMiddleware(x_api_key="DEN#3xTezZDo1nJg1pO$tIrzQ9A")

# Routers for different route groups
admin_router = APIRouter(dependencies=[Depends(guard.protect)])
settings_router = APIRouter(dependencies=[Depends(guard.protect)])
public_router = APIRouter()

# General routes
@app.get("/", tags=["General"])
async def root():
    return {"message": "Hello World"}

@app.get("/health", tags=["General"])
async def health():
    return {"status": "healthy"}

# Public routes
@public_router.get("/public", tags=["Public"])
async def public():
    return {"message": "This is a public endpoint accessible to everyone."}

# Admin routes
@admin_router.get("/admin", tags=["Admin"])
async def admin():
    return {"message": "Welcome to the admin area!"}

# Settings routes
@settings_router.get("/settings", tags=["Settings"])
async def settings():
    return {"message": "Settings page, accessible only to authorized users."}

# Include the routers in the main app
app.include_router(public_router)
app.include_router(admin_router, prefix="/secure")
app.include_router(settings_router, prefix="/secure")
```

### Making Requests

```bash
# Unauthorized request (missing API key)
curl -X GET http://localhost:8000/secure/admin
# Response: {"detail": "X-API-Key header missing"}
# Status code: 401

# Unauthorized request (invalid API key)
curl -X GET http://localhost:8000/secure/admin -H "X-API-Key: wrong-key"
# Response: {"detail": "Invalid X-API-Key"}
# Status code: 403

# Authorized request
curl -X GET http://localhost:8000/secure/admin -H "X-API-Key: YOUR_API_KEY"
# Response: {"message": "Welcome to the admin area!"}
# Status code: 200
```

## Demo

```bash
git clone https://github.com/anqorithm/xapi-guard-middleware.git
cd xapi-guard-middleware
poetry install
poetry run uvicorn app:app --reload
```

* The FastAPI app is protected by the XAPI Guard Middleware
![image](./assets/1.png)

* X-API-Key header is missing
![image](./assets/2.png)

* X-API-Key header is invalid
![image](./assets/3.png)
![image](./assets/4.png)

* X-API-Key header is valid
![image](./assets/5.png)
![image](./assets/6.png)


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
## Contributors

- [Abdullah Alqahtani](https://github.com/anqorithm)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
