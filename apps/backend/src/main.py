from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager # Lifespan ke liye
from .api import auth, tasks
from .database.database import engine
from .models import user, task
from sqlmodel import SQLModel
import asyncio

# Create the rate limiter
limiter = Limiter(key_func=get_remote_address)

# Database tables create karne ke liye naya tarika (Async compatible)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    # Agar aap asyncpg use kar rahe hain toh create_all ko run_sync mein chalana parta hai
    def create_db_and_tables():
        SQLModel.metadata.create_all(bind=engine)
    
    # Isay startup par chalayein
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, create_db_and_tables)
    yield
    # Shutdown logic yahan aa sakti hai

# Create the FastAPI app with lifespan
app = FastAPI(
    title="Todo API",
    description="Full-Stack Todo Web Application API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    lifespan=lifespan # on_event ki jagah lifespan use karein
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin"]
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Include API routers
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}