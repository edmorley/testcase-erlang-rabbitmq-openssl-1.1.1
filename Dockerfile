# python:3.7.4-slim-stretch -> openssl 1.1.0
# python:3.7.4-slim-buster -> openssl 1.1.1
FROM python:3.7.4-slim-buster

RUN pip install --no-cache-dir celery==4.3.0 kombu==4.6.3 amqp==2.5.0

WORKDIR /app
COPY celery_config.py .
CMD celery worker --config=celery_config --loglevel=info
