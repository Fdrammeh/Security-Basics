# exercises/security-basics/app/main.py
# L10 — Security Hardened API
#
# Run with: uvicorn app.main:app --reload  (from security-basics/ folder)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# TODO: Import CORSMiddleware from fastapi.middleware.cors
from fastapi.middleware.cors import CORSMiddleware

# TODO: Import the items router
from app.routers import items
import time


app = FastAPI(title="Security Basics API")

# TODO: Add CORS middleware
# Key concept: CORS (Cross-Origin Resource Sharing) controls which web origins
# can make requests to your API from a browser.
# NEVER use allow_origins=["*"] in production — it allows any website to call
# your API with the user's cookies/credentials.
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501", 
        "https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH","DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# TODO: Add rate limiting middleware
# Track request counts per IP in a simple dict
# Return 429 Too Many Requests if a single IP exceeds 10 requests per minute
# Hint: use a dict like request_counts: dict[str, list[float]] = {}
# Store timestamps of requests per IP, filter to last 60 seconds

request_counts: dict[str, list[float]] = {}
MAX_REQUESTS = 10
TIME_WINDOW = 60

@app.middleware("http")
async def rate_limit(request: Request, call_next):

    # Get the client's IP address 
    client_ip = request.client.host

    # Get the current time
    current_time = time.time()

    # If this IP has never made a request before, # create an empty list for it.
    if client_ip not in request_counts: request_counts[client_ip] = []

    # Keep only requests from the last 60 seconds
    request_counts[client_ip] = [ 
        timestamp 
        for timestamp in request_counts[client_ip] 
        if current_time - timestamp < TIME_WINDOW ]

    # Check whether the IP has reached the limit 
    if len(request_counts[client_ip]) >= MAX_REQUESTS:  
        return JSONResponse( 
            status_code=429, 
            content={ "detail": "Too many requests. Please try again later." } )

    # Record this request 
    request_counts[client_ip].append(current_time)

    # Continue to the actual endpoint 
    response = await call_next(request)

    return response

# TODO: Include the items router
app.include_router(items.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)