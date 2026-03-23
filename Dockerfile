FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry

ADD pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY /app/* .
COPY app/alembic.ini .

CMD ["uvicorn", "presentation.api.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
