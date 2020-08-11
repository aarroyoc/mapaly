FROM python:3.8.5

WORKDIR /opt/mapaly

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .
