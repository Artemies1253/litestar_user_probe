FROM python:3.12.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src
ENV PYTHONPATH="/src:${PYTHONPATH}"
RUN apt-get update && apt-get install -y gcc python3-dev musl-dev postgresql-server-dev-all

ENV POETRY_VIRTUALENVS_CREATE=false
COPY pyproject.toml /src/pyproject.toml
RUN pip install --upgrade pip && pip install poetry && poetry update

COPY src /src

CMD ["tail", "-f", "/dev/null"]
