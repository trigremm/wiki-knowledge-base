FROM python:3.12.7-slim-bookworm

ARG UV_VERSION=0.5.5

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV UV_NO_CACHE=1
ENV UV_SYSTEM_PYTHON=1
ENV UV_VIRTUALENV=0

WORKDIR /app

RUN apt update && \
    apt install -y curl make

RUN pip install --upgrade uv==${UV_VERSION}
COPY pyproject.toml .
RUN uv pip install .

COPY ../template_project .

ENTRYPOINT ["sleep", "infinity"]
