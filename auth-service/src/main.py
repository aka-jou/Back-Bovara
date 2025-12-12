from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.infrastructure.config.settings import get_settings
from src.infrastructure.config.database import engine, Base
from src.infrastructure.adapters.inbound.http.auth_controller import router as auth_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle: Startup y Shutdown"""
    # Startup: Crear tablas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Base de datos inicializada")
    
    yield
    
    # Shutdown
    await engine.dispose()
    print("Conexión a DB cerrada")


# Crear aplicación
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Microservicio de autenticación para Bovara",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS para Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Health"])
async def root():
    """Health check"""
    return {
        "service": settings.PROJECT_NAME,
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check detallado"""
    return {
        "status": "healthy",
        "database": "connected",
        "service": "auth-service"
    }
    
    
    # Configurar CORS para permitir peticiones desde la app móvil
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:*",  # Para emulador Android
        "http://10.0.2.2:*",   # IP especial del emulador Android
        "http://127.0.0.1:*",  # Para emulador iOS
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    
    
