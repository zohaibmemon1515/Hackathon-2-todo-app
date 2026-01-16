from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api import auth, tasks, chat  # <-- 1. Chat import add kiya
from .database.database import engine
from .models import user, task
from sqlmodel import SQLModel
import asyncio

# Create the rate limiter
limiter = Limiter(key_func=get_remote_address)

# Database tables creation logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    def create_db_and_tables():
        SQLModel.metadata.create_all(bind=engine)
    
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, create_db_and_tables)
    yield

# Create the FastAPI app
app = FastAPI(
    title="Todo API",
    description="Full-Stack Todo Web Application API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    lifespan=lifespan
)

# Rate Limiter Setup
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# CORS Middleware (Frontend communication ke liye zaroori)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin"]
)

# Security Headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# --- 2. API ROUTERS REGISTRATION ---
# Note: Hum prefix "/api/v1" use kar rahe hain consistent rehne ke liye
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"]) # <-- 3. Chat register ho gaya

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}