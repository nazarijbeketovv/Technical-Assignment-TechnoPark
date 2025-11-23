from fastapi import APIRouter
from api.v1.handlers.products import router as products_router

router = APIRouter(prefix="/v1")
router.include_router(products_router)
