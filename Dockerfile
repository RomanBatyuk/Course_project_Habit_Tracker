FROM python:3.13-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Копирование проекта
COPY . /app
WORKDIR /app
RUN mkdir -p /app/staticfiles /app/media

# Entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]