FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

COPY --from=ghcr.io/astral-sh/uv:0.7.12 /uv /uvx /bin/

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    gcc \
    make

WORKDIR /app

RUN ln -s /app /app/src || true

COPY uv.lock pyproject.toml ./
RUN uv venv && uv sync

COPY alembic.ini ./
COPY ./src .
COPY Makefile ./

EXPOSE 8000

CMD [ "python3", "-m", "main" ]
