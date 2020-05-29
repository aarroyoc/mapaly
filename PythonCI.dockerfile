FROM python:3.8.3

WORKDIR /opt/mapaly

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

RUN pip install flake8==3.8.2 pytest==5.4.2

COPY . .