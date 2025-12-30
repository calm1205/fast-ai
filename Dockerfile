FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apt-get update && apt-get install -y sqlite3

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY .sqliterc /root/.sqliterc

COPY src ./src
