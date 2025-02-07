from http import HTTPStatus
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from .error_codes import APIErrorCode


class XAPIGuardMiddleware:
    """
    Middleware to protect routes with an API key.

    Attributes:
        x_api_key (str): The valid API key for authentication.
        x_api_key_header (APIKeyHeader): The FastAPI security dependency for API key header.
    """

    def __init__(self, x_api_key: str):
        """
        Initializes the XAPIGuardMiddleware with the provided API key.

        Args:
            x_api_key (str): The valid API key to be used for authentication.
        """
        self.x_api_key = x_api_key
        self.x_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

    async def protect(
        self, x_api_key: str = Depends(APIKeyHeader(name="X-API-Key", auto_error=True))
    ):
        """
        Protects a route by validating the provided API key.

        Args:
            x_api_key (str): The API key provided in the request header.

        Raises:
            HTTPException: If the API key is invalid, a 403 Forbidden error is raised.
        """
        if x_api_key != self.x_api_key:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail={
                    "code": APIErrorCode.INVALID_API_KEY.value,
                    "message": "Invalid API key",
                },
            )
