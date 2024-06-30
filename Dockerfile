FROM python:3.11-bullseye
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --only main

COPY . /app

CMD celery -A app.tasks worker --loglevel=info & uvicorn app.main:app --host 0.0.0.0 --port 8000