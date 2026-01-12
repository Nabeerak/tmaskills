# CORS Configuration and Security

## Table of Contents

- [What is CORS?](#what-is-cors)
- [Basic CORS Setup](#basic-cors-setup)
- [Configuration Options](#configuration-options)
- [Environment-Based Configuration](#environment-based-configuration)
- [Security Considerations](#security-considerations)
- [Development vs Production](#development-vs-production)
- [Multiple Subdomain Support](#multiple-subdomain-support)
- [Custom Headers](#custom-headers)
- [Authentication with CORS](#authentication-with-cors)
- [Preflight Requests](#preflight-requests)
- [Troubleshooting CORS Errors](#troubleshooting-cors-errors)
- [Best Practices Summary](#best-practices-summary)

---

## What is CORS?

Cross-Origin Resource Sharing (CORS) is a security feature that restricts web pages from making requests to a different domain than the one serving the web page.

---

## Basic CORS Setup

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Configuration Options

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `allow_origins` | List[str] | Allowed origin URLs | `["http://localhost:3000"]` |
| `allow_credentials` | bool | Allow cookies/auth headers | `True` |
| `allow_methods` | List[str] | Allowed HTTP methods | `["GET", "POST"]` or `["*"]` |
| `allow_headers` | List[str] | Allowed request headers | `["*"]` or `["Content-Type"]` |
| `expose_headers` | List[str] | Headers accessible to browser | `["X-Total-Count"]` |
| `max_age` | int | Cache preflight response (seconds) | `600` |

---

## Environment-Based Configuration

**Recommended**: Load CORS origins from environment variables.

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "My API"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# app/main.py
from app.core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**.env file**:
```bash
# Development
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]

# Production
BACKEND_CORS_ORIGINS=["https://myapp.com","https://www.myapp.com"]
```

---

## Security Considerations

### 1. Never Use Wildcard with Credentials

**INSECURE**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ❌ Wildcard
    allow_credentials=True,  # ❌ With credentials
)
```

Browsers will **reject** this configuration. It's a security violation.

### 2. Specify Exact Origins in Production

**Development** (permissive):
```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
]
```

**Production** (strict):
```python
allow_origins=[
    "https://myapp.com",
    "https://www.myapp.com",
    "https://app.myapp.com",
]
```

### 3. Use HTTPS in Production

Always use `https://` in production CORS origins:
```python
# ❌ Development only
allow_origins=["http://myapp.com"]

# ✅ Production
allow_origins=["https://myapp.com"]
```

### 4. Limit Allowed Methods

Only allow methods your API uses:
```python
# ❌ Too permissive
allow_methods=["*"]

# ✅ Explicit
allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
```

### 5. Limit Exposed Headers

Only expose headers frontend needs:
```python
# Expose custom pagination header
expose_headers=["X-Total-Count", "X-Page-Count"]
```

---

## Development vs Production

### Development Setup

```python
# app/core/config.py
class Settings(BaseSettings):
    ENVIRONMENT: str = "development"

    @property
    def CORS_ORIGINS(self) -> List[str]:
        if self.ENVIRONMENT == "development":
            return [
                "http://localhost:3000",
                "http://localhost:8000",
                "http://127.0.0.1:3000",
                "http://0.0.0.0:3000",
            ]
        else:
            # Production origins from environment
            return self.BACKEND_CORS_ORIGINS

settings = Settings()

# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Multiple Subdomain Support

### Pattern Matching (Manual)

```python
from fastapi import Request

def get_cors_origins(request: Request) -> List[str]:
    """Get allowed origins based on request."""
    origin = request.headers.get("origin", "")

    # Allow all myapp.com subdomains
    if origin.endswith(".myapp.com") or origin == "https://myapp.com":
        return [origin]

    # Fallback to configured origins
    return settings.BACKEND_CORS_ORIGINS

# Custom CORS middleware
from starlette.middleware.cors import CORSMiddleware as _CORSMiddleware

class DynamicCORSMiddleware(_CORSMiddleware):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            origin = headers.get(b"origin", b"").decode()

            if origin.endswith(".myapp.com"):
                self.allow_origins = [origin]

        await super().__call__(scope, receive, send)
```

### Regex Pattern (Third-Party)

Use `fastapi-cors` package for regex support:
```bash
pip install fastapi-cors
```

```python
from fastapi_cors import CORS

CORS(
    app,
    allow_origin_regex=r"https://.*\.myapp\.com",
    allow_credentials=True,
)
```

---

## Custom Headers

### Sending Custom Headers

```python
@router.get("/tasks")
def get_tasks(
    response: Response,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get tasks with pagination headers."""
    # Get total count
    total = session.exec(select(func.count()).select_from(Task)).one()

    # Get tasks
    tasks = session.exec(
        select(Task).offset(skip).limit(limit)
    ).all()

    # Add custom headers
    response.headers["X-Total-Count"] = str(total)
    response.headers["X-Page-Size"] = str(limit)

    return tasks

# Expose headers in CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    expose_headers=["X-Total-Count", "X-Page-Size"],  # Make headers accessible to browser
)
```

### Frontend Access

```javascript
// Frontend code
fetch('http://localhost:8000/api/v1/tasks')
  .then(response => {
    const total = response.headers.get('X-Total-Count');
    const pageSize = response.headers.get('X-Page-Size');
    return response.json();
  })
```

---

## Authentication with CORS

### Cookie-Based Authentication

```python
# Enable credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],
    allow_credentials=True,  # Required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set cookies in response
@router.post("/login")
def login(response: Response, credentials: LoginCredentials):
    # Validate credentials
    token = create_access_token(user.id)

    # Set cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # Prevent JavaScript access
        secure=True,  # HTTPS only
        samesite="lax",  # CSRF protection
        max_age=3600
    )

    return {"message": "Logged in"}
```

### Bearer Token Authentication

```python
# Frontend sends token in header
Authorization: Bearer <token>

# Backend accepts token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@router.get("/me")
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    # Validate token
    ...
```

---

## Preflight Requests

CORS preflight is an OPTIONS request sent before actual request.

### How Preflight Works

```
1. Browser sends OPTIONS request
   OPTIONS /api/v1/tasks
   Origin: http://localhost:3000
   Access-Control-Request-Method: POST
   Access-Control-Request-Headers: Content-Type

2. Server responds with allowed origins/methods
   Access-Control-Allow-Origin: http://localhost:3000
   Access-Control-Allow-Methods: POST, GET, OPTIONS
   Access-Control-Allow-Headers: Content-Type
   Access-Control-Max-Age: 600

3. If allowed, browser sends actual request
   POST /api/v1/tasks
```

### Caching Preflight

Reduce preflight requests by caching:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600  # Cache preflight for 10 minutes
)
```

---

## Troubleshooting CORS Errors

### Common Error Messages

**"No 'Access-Control-Allow-Origin' header"**
```python
# Fix: Add CORS middleware
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"])
```

**"Credentials flag is true, but Access-Control-Allow-Credentials is not 'true'"**
```python
# Fix: Enable credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True  # Add this
)
```

**"The value of the 'Access-Control-Allow-Origin' header must not be the wildcard '*' when credentials flag is true"**
```python
# Fix: Use specific origins, not wildcard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Not ["*"]
    allow_credentials=True
)
```

### Debug CORS Issues

```python
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_cors(request: Request, call_next):
    """Log CORS-related headers."""
    origin = request.headers.get("origin")
    if origin:
        logger.info(f"CORS request from origin: {origin}")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request path: {request.url.path}")

    response = await call_next(request)

    # Log response CORS headers
    cors_headers = {
        k: v for k, v in response.headers.items()
        if k.lower().startswith("access-control")
    }
    if cors_headers:
        logger.info(f"CORS response headers: {cors_headers}")

    return response
```

---

## Best Practices Summary

1. ✅ Use environment variables for CORS origins
2. ✅ Never use wildcard (`*`) with credentials in production
3. ✅ Use HTTPS in production
4. ✅ Specify exact allowed origins
5. ✅ Limit methods to what API actually uses
6. ✅ Cache preflight requests with `max_age`
7. ✅ Expose only necessary custom headers
8. ✅ Test CORS in both development and production environments
9. ❌ Don't expose internal error details in CORS responses
10. ❌ Don't allow all origins in production
