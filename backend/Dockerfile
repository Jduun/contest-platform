FROM python:3.10-slim

WORKDIR /backend

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root 
    #--without dev

ENV PYTHONPATH=/backend

COPY . /backend