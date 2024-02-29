FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.0

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/* && \
    pip install "poetry==$POETRY_VERSION"

WORKDIR /gash/

COPY ./poetry.lock ./pyproject.toml /gash/

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

COPY src/ /gash/src/
COPY policy/ /gash/policy/