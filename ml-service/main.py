from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import clustering_routes, forecasting_routes

app = FastAPI(
    title="Bovara ML Service",
    description="Servicio de Machine Learning para clustering y forecasting multimodal de ganado",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "Bovara ML Service",
        "version": "3.0.0",
        "endpoints": {
            "clustering": {
                "train": "/api/v1/clustering/train",
                "predict": "/api/v1/clustering/predict/{cattle_id}",
                "all": "/api/v1/clustering/all"
            },
            "forecasting": {
                "train": "/api/v1/forecasting/train",
                "predict": "/api/v1/forecasting/predict/{cattle_id}"
            }
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ml-service"}


# Incluir routers
app.include_router(clustering_routes.router, prefix="/api/v1")
app.include_router(forecasting_routes.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
