
import logging

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app import models

from app.routers import (
    auth,
    doctors,
    patients
)


# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# =========================
# DATABASE
# =========================

Base.metadata.create_all(
    bind=engine
)


# =========================
# FASTAPI
# =========================

app = FastAPI(
    title="Doctor Patient Management API",
    description="Production-style FastAPI backend",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# =========================
# ROUTES
# =========================

app.include_router(
    auth.router
)

app.include_router(
    doctors.router
)

app.include_router(
    patients.router
)


@app.get("/")
def home():

    return {
        "message": "Doctor Patient Management API is running"
    }