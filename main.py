import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

from core.config import settings
from routers import story, job
from db.database import create_tables

create_tables()

app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# This configuration allows requests from the origins defined in settings.ALLOWED_ORIGINS and supports all HTTP methods and headers for cross-origin requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # E.g., "https://adventure-ai-seven.vercel.app"
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allows Content-Type, Authorization, etc.
)
# -------------------------------------------------------------

app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)

# Default port configuration
DEFAULT_PORT = int(os.getenv("PORT", 8000))
DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")

if __name__ == "__main__":
    import uvicorn
    # Using host="0.0.0.0" is important for container/server deployments like Render
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)