# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import api_router
from src.infrastructure.database import Base, engine


# Crear tablas
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bovara Core Service",
    description="Microservicio de gestión de ganado y ranchos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Bovara Core Service API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "core-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
