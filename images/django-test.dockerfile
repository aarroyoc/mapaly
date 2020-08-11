FROM python:3.8.5

WORKDIR /opt/mapaly

RUN python -m pip install poetry

COPY . .

RUN poetry install --no-root

ENTRYPOINT ["poetry", "run"]