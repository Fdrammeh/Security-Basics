# exercises/security-basics/app/main.py
# L10 — Security Hardened API
#
# Run with: uvicorn app.main:app --reload  (from security-basics/ folder)

"""
Security Basics API — Security Measures

1. CORS:
   Only configured browser origins are allowed.

2. Rate limiting:
   SlowAPI limits requests by client IP:
   - Login: 5 requests per minute.
   - POST/create: 20 requests per minute.
   - GET/list: 60 requests per minute.
   Excess requests receive HTTP 429.

3. Input validation:
   Pydantic schemas enforce field types, maximum lengths,
   and numeric ranges where applicable.

4. Input sanitization:
   Item text is trimmed and HTML tags are removed.

5. SQL injection prevention:
   Database queries should use SQLAlchemy expressions
   or parameterized queries instead of string concatenation.

Note: Rate limiting and validation complement one another;
they do not replace authentication or database security.
"""



from fastapi import FastAPI
#from fastapi.responses import JSONResponse

# TODO: Import CORSMiddleware from fastapi.middleware.cors
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
# TODO: Import the items router
from app.routers import items

app = FastAPI(title="Security Basics API")

# Configure SlowAPI
app.state.limiter = items.limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501", 
        "https://localhost:3000",
    ],    
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH","DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include the items router
app.include_router(items.router, prefix="/items", tags=["Items"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
