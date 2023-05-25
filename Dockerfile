FROM python:3.11-slim-buster AS requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY pyproject.toml poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY --from=requirements-stage /tmp/requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

COPY services/web /usr/src/app/