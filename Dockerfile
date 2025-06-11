FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app
RUN pip install .

COPY ./src /app
COPY ./.env /app

RUN python /app/manage.py collectstatic --no-input
