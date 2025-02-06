from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from http import HTTPMethod


class XAPIGuard:
    def __init__(self, app):
        self.app = app
        self.api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
        self.method_map = {
            HTTPMethod.GET: self.app.get,
            HTTPMethod.POST: self.app.post,
            HTTPMethod.PUT: self.app.put,
            HTTPMethod.DELETE: self.app.delete,
            HTTPMethod.PATCH: self.app.patch,
            HTTPMethod.OPTIONS: self.app.options,
            HTTPMethod.HEAD: self.app.head,
            HTTPMethod.TRACE: self.app.trace,
        }

    def protect(self, path: str, method: HTTPMethod = HTTPMethod.GET, *args, **kwargs):
        """
        Decorator to protect an endpoint using a dynamic HTTP method.
        Uses standard HTTP methods from Python's http module.

        Example usage:
          @api_guard.protect("/protected", method=HTTPMethod.POST)
          async def protected_route():
              return {"message": "protected"}
        """

        def decorator(func):
            async def wrapper(api_key: str = Security(self.api_key_header)):
                if not api_key:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Could not validate API Key",
                    )
                return await func()

            if method not in self.method_map:
                raise ValueError(f"Unsupported HTTP method: {method}")

            return self.method_map[method](path, *args, **kwargs)(wrapper)

        return decorator
