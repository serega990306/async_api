FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip
RUN  pip install -r requirements.txt

COPY . .


ENTRYPOINT ["./index_schema.sh"]