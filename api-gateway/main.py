# api-gateway/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Bovara API Gateway", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs de servicios
AUTH_SERVICE_URL = "http://localhost:8000"
CORE_SERVICE_URL = "http://localhost:8001"
REQUEST_TIMEOUT = 30.0


@app.get("/")
async def root():
    """Endpoint raíz del gateway"""
    return {
        "service": "Bovara API Gateway",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check del gateway - NO REDIRIGE"""
    services_status = {}
    
    # Check Auth Service
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{AUTH_SERVICE_URL}/health")
            services_status["auth_service"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        services_status["auth_service"] = "unreachable"
    
    # Check Core Service
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{CORE_SERVICE_URL}/health")
            services_status["core_service"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        services_status["core_service"] = "unreachable"
    
    return {
        "gateway": "healthy",
        "services": services_status
    }


@app.api_route(
    "/api/v1/auth/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def auth_proxy(request: Request, path: str):
    """Proxy para Auth Service - Solo /api/v1/auth/*"""
    try:
        target_url = f"{AUTH_SERVICE_URL}/api/v1/auth/{path}"
        logger.info(f"🔵 [AUTH] {request.method} /api/v1/auth/{path}")
        
        headers = dict(request.headers)
        headers.pop("host", None)
        body = await request.body()
        
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params
            )
        
        logger.info(f"✅ [AUTH] {response.status_code}")
        
        return JSONResponse(
            content=response.json() if response.content else {},
            status_code=response.status_code
        )
    
    except httpx.ConnectError:
        logger.error("❌ Auth Service no disponible")
        raise HTTPException(status_code=503, detail="Auth Service no disponible")
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.api_route(
    "/api/v1/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def core_proxy(request: Request, path: str):
    """Proxy para Core Service - Todo /api/v1/* EXCEPTO /api/v1/auth/*"""
    try:
        target_url = f"{CORE_SERVICE_URL}/api/v1/{path}"
        logger.info(f"🟢 [CORE] {request.method} /api/v1/{path}")
        
        headers = dict(request.headers)
        headers.pop("host", None)
        body = await request.body()
        
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params
            )
        
        logger.info(f"✅ [CORE] {response.status_code}")
        
        return JSONResponse(
            content=response.json() if response.content else {},
            status_code=response.status_code
        )
    
    except httpx.ConnectError:
        logger.error("❌ Core Service no disponible")
        raise HTTPException(status_code=503, detail="Core Service no disponible")
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")
