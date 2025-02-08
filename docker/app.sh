#!/bin/bash

echo "Запуск миграций..."
alembic upgrade head || { echo "Ошибка при выполнении миграций."; exit 1; }

# Запуск приложения
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
