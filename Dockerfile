
########## BUILDER ##########
FROM python:3.12-slim AS builder
ENV PATH="/app/.venv/bin:$PATH" UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/


COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project

COPY app ./app
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen

########## RUNTIME ##########
FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1 PATH="/app/.venv/bin:$PATH" PYTHONPATH=/app
WORKDIR /app

# Пользователь без root
RUN useradd -r -u 10001 appuser

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app /app/app


EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=5 \
  CMD python -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1',8000))" || exit 1

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
