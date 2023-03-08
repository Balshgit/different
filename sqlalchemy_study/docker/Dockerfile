
FROM --platform=linux/amd64 python:3.11.1

ARG USER

ENV SOURCE_DIR=/app/src/

ENV USER=${USER} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="${PYTHONPATH}:${SOURCE_DIR}" \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.poetry/bin"

RUN printf "================\n\nStart build app. USER is: "${USER}"\n\n===============\n" \
  && apt-get update \
  && apt-get install --no-install-recommends -y \
    procps \
    bash \
    build-essential \
    curl \
    iputils-ping \
    gettext \
    git \
    libpq-dev \
    nano \
    sshpass \
  && pip install --upgrade pip \
  # Installing `poetry` package manager:
  && pip install poetry \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR ${SOURCE_DIR}

RUN if [ "$USER" != "root" ]; then \
      groupadd -r "$USER" && useradd -d /home/"$USER" -r -g "$USER" "$USER" \
      && chown "$USER":"$USER" -R /home/"$USER"; \
    fi

COPY --chown="$USER":"$USER" ./poetry.lock ./pyproject.toml ${SOURCE_DIR}

# Installing requirements
RUN poetry install && rm -rf "$POETRY_CACHE_DIR"

COPY ./docker/scripts/ /app/scripts/
RUN chmod +x /app/scripts/docker-entrypoint.sh /app/scripts/alembic-init-migrate.sh

USER "$USER"

# Copying actuall application
COPY --chown="$USER":"$USER" . ${SOURCE_DIR}
