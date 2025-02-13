#!/bin/bash

echo "Создаю миграцию Alembic..."
alembic revision --autogenerate -m "initial migration"
echo "Миграция создана!"

echo "Запуск миграций..."
alembic upgrade head || { echo "Ошибка при выполнении миграций."; exit 1; }
echo "Миграция прошла успешно!"

# Запуск приложения
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
