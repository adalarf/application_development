FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/src/app/.venv/bin:$PATH"

WORKDIR /usr/src/app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./

RUN uv sync --no-cache

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
