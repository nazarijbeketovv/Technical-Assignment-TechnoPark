Сделать маленький сервис расчёта стоимости изделия

Функционал

I. На вход POST-эндпоинт /calc принимает JSON:
{
"materials": [
{"name": "steel", "qty": 120, "price_rub": 54.5},
{"name": "copper", "qty": 12.3, "price_rub": 640.0}
]
}

II. Сервис должен

1. Проверить входные данные (Pydantic),
2. Рассчитать total_cost_rub = sum(qty * price_rub),
3. Сохранить результат в Postgres таблицу:
   calc_results(id SERIAL, total_cost_rub NUMERIC, created_at TIMESTAMP)
4. Вернуть { "total_cost_rub": ... }.

Требования:

- FastAPI
- SQLAlchemy / asyncpg
- Pydantic-схемы



