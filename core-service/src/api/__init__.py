from fastapi import APIRouter
from src.api.v1 import api_router

api_router_main = APIRouter()
api_router_main.include_router(api_router)
