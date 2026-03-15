FROM python:3.12-sli

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . .

RUN if [ ! -f .env ] && [ -f .env.example ]; then \
        cp .env.example .env; \
    fi

RUN uv sync --frozen --no-cache

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]