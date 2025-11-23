from fastapi import FastAPI
import uvicorn
from api import router as api_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
