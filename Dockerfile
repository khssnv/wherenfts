FROM python:3.10-bullseye

ENV LOGURU_LEVEL ERROR
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.1.13

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /wherenfts/

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi
COPY . ./

ENTRYPOINT ["python", "-m", "wherenfts"]
