from fastapi import APIRouter
from app.api.v1 import auth, news, category

api_v1_router = APIRouter(prefix="/api/v1")

# incluye subrutas
api_v1_router.include_router(auth.router)
api_v1_router.include_router(news.router)
api_v1_router.include_router(category.router)

