# Используем официальный Python образ
FROM python:3.9-slim

# Создадим рабочую директорию
WORKDIR /app

# Скопируем requirements.txt
COPY requirements.txt .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем всё остальное
COPY . .

# Открываем порт 8000 (по умолчанию Django слушает 8000)
EXPOSE 8000

# Запуск через Gunicorn (или python manage.py runserver)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]