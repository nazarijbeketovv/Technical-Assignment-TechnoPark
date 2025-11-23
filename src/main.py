"""Точка входа FastAPI-приложения для расчёта стоимости изделия."""

from fastapi import FastAPI
import uvicorn
from api import router as api_router


def create_app() -> FastAPI:
    """Создать и сконфигурировать экземпляр FastAPI-приложения."""
    app = FastAPI(
        title='Тестовое задание для компании "Технопарк"',
        version="1.0.0",
    )
    app.include_router(api_router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
