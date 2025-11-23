from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def root() -> dict[str, str]:
    return {"msg": "Hello from root!"}
