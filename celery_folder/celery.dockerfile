FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /celery_application

COPY requirements.txt /celery_application/

RUN pip install -r requirements.txt

COPY . /celery_application/

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=INFO"]