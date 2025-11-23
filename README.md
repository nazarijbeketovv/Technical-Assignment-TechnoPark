## Product Calculator

Сервис на FastAPI для расчёта итоговой стоимости изделия на основе списка материалов.

### Запуск проекта

1. **Скопировать env-файл**

```bash
make env
```

Команда создаст файл `.env` из шаблона `.env.template`. При необходимости отредактируйте `.env` (например, параметры подключения к БД).

2. **Запустить сервисы в Docker**

```bash
docker compose up --build
```

- **Что делает команда**: собирает образ приложения, поднимает контейнер с Postgres, применяет Alembic-миграции и запускает FastAPI-приложение.
- После успешного старта API будет доступен по адресу `http://localhost:8000`.

### Примеры запросов (curl)

Базовый URL для API: `http://localhost:8000/api/v1/calc`  
Метод: `POST`  
Заголовок: `Content-Type: application/json`

1. **Простой расчёт с одним материалом**

```bash
curl -X POST "http://localhost:8000/api/v1/calc" \
  -H "Content-Type: application/json" \
  -d '{
    "materials": [
      { "name": "Дерево", "qty": 2, "price_rub": 150.50 }
    ]
  }'
```

2. **Изделие из нескольких материалов**

```bash
curl -X POST "http://localhost:8000/api/v1/calc" \
  -H "Content-Type: application/json" \
  -d '{
    "materials": [
      { "name": "Металл", "qty": 3.5, "price_rub": 420.00 },
      { "name": "Пластик", "qty": 1.2, "price_rub": 95.75 }
    ]
  }'
```

3. **Использование десятичных количеств и цен**

```bash
curl -X POST "http://localhost:8000/api/v1/calc" \
  -H "Content-Type: application/json" \
  -d '{
    "materials": [
      { "name": "Краска", "qty": 0.75, "price_rub": 300.99 },
      { "name": "Грунтовка", "qty": 1.25, "price_rub": 199.49 }
    ]
  }'
```

4. **Большие количества (нагрузочный пример)**

```bash
curl -X POST "http://localhost:8000/api/v1/calc" \
  -H "Content-Type: application/json" \
  -d '{
    "materials": [
      { "name": "Сталь листовая", "qty": 1000, "price_rub": 59.90 },
      { "name": "Болты", "qty": 5000, "price_rub": 3.15 }
    ]
  }'
```

5. **Минимально валидный запрос**

```bash
curl -X POST "http://localhost:8000/api/v1/calc" \
  -H "Content-Type: application/json" \
  -d '{
    "materials": [
      { "name": "Тестовый материал", "qty": 1, "price_rub": 0 }
    ]
  }'
```

### Пример SQL-запроса

Один SQL-запрос, который возвращает **10 последних расчётов**, отсортированных по дате создания (от самых новых к более старым), из таблицы `calc_results`:

SELECT
    id,
    total_cost_rub,
    created_at
FROM calc_results
ORDER BY created_at DESC
LIMIT 10;