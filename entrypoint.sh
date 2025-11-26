#!/bin/sh
set -e

# Шаг 1: Ждём, пока PostgreSQL будет доступен
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Шаг 2: Запускаем миграции
python manage.py migrate

# Шаг 3: Собираем статические файлы
python manage.py collectstatic --noinput

# Шаг 4: Создаём суперпользователя
python manage.py createsuperuser --noinput --username admin --email admin@example.com

# Шаг 5: Запускаем основной процесс
exec "$@"
