FROM python:3.11-bullseye
RUN mkdir /app

COPY pyproject.toml /app

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --only main

COPY . /app

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
