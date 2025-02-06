from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from http import HTTPStatus


class XApiKeyMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for API key authentication.

    This middleware validates the x-api-key header against a predefined API key.
    Requests to excluded paths bypass the validation.

    Args:
        app: The FastAPI application
        api_key: The API key to validate against
        exclude_paths: Set of paths to exclude from validation
    """

    def __init__(self, app, api_key: str, exclude_paths: set = None):
        """Initialize the middleware.

        Args:
            app: The FastAPI application
            api_key: The API key to validate against
            exclude_paths: Set of paths to exclude from validation

        Raises:
            ValueError: If api_key is empty
        """
        super().__init__(app)
        if not api_key:
            raise ValueError("API key cannot be empty")
        self.api_key = api_key
        self.exclude_paths = exclude_paths or set()

    async def dispatch(self, request, call_next):
        """Validate the x-api-key header in the request.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            Response: The response from the next middleware or an error response

        Response Codes:
            200: Request successful
            401: API key missing
            403: Invalid API key
            500: Internal server error
        """
        try:
            if request.url.path in self.exclude_paths:
                return await call_next(request)

            api_key = request.headers.get("X-API-Key")

            if not api_key:
                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    content={"detail": "X-API-Key header missing"},
                )

            if api_key != self.api_key:
                return JSONResponse(
                    status_code=HTTPStatus.FORBIDDEN,
                    content={"detail": "Invalid X-API-Key"},
                )

            response = await call_next(request)
            return response

        except Exception:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"},
            )
