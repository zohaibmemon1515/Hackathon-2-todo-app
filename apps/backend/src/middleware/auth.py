from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..auth.jwt import verify_token


security = HTTPBearer()


async def jwt_validation_middleware(request: Request, call_next):
    """
    Middleware to validate JWT token for protected routes
    """
    # Define public routes that don't require authentication
    public_routes = ["/", "/health", "/docs", "/redoc", "/api/v1/auth/register", "/api/v1/auth/login"]

    # Check if the current route is public
    if request.url.path in public_routes:
        response = await call_next(request)
        return response

    # For protected routes, check for JWT token
    if request.url.path.startswith("/api/v1/auth/refresh"):
        # Refresh token might have different logic
        response = await call_next(request)
        return response

    # For all other routes, require authentication
    try:
        # Get the authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract token
        token = auth_header.split(" ")[1]

        # Verify the token
        payload = verify_token(token)

        # Add user info to request state for use in endpoints
        request.state.user_email = payload.get("sub")
        request.state.user_id = payload.get("user_id")  # if included in token

    except HTTPException:
        # Re-raise HTTP exceptions (like invalid token)
        raise
    except Exception as e:
        # Handle other exceptions (like token decoding errors)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response = await call_next(request)
    return response