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
![image](./assets/5.png)

* Authorized request
![image](./assets/3.png)

* OpenAPI/Swagger documentation
![image](./assets/4.png)



## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
## Contributors

- [Abdullah Alqahtani](https://github.com/anqorithm)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
