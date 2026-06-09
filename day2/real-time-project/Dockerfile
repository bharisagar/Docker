FROM python:3.11-slim

ARG APP_VERSION=1.0
ARG APP_ENV=production

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV APP_VERSION=${APP_VERSION}
ENV APP_ENV=${APP_ENV}
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
