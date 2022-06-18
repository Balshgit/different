FROM python:3.9.10

# python:
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.13 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.poetry/bin"

RUN apt update \
  && apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    nano \
  && export TERM=xterm \
  # Installing `poetry` package manager:
#  # https://github.com/python-poetry/poetry
#  && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
  && pip install --upgrade pip \
  && pip install poetry

COPY ./pyproject.toml /code/

WORKDIR /code

RUN export PATH="/root/.local/bin:$PATH" \
  && poetry --version \
  && poetry lock \
  && poetry export -f requirements.txt --without-hashes --output requirements.txt

WORKDIR /poetry



