# Course_project_Habit_Tracker


## Описание:

Course_project_Habit_Tracker - курсовой проект по Django "Трекер привычек".

## Установка:

1. Клонируйте репозиторий:
```
https://github.com/RomanBatyuk/Course_project_Habit_Tracker
```
2. Установите зависимости:
```
pip install -r requirements.txt
```

## Локальный запуск:

Клонируйте репозиторий:
- git clone https://github.com/roman/course_project_habit_tracker.git
- cd course_project_habit_tracker

Соберите и запустите контейнеры:
- docker-compose build --no-cache  # Первая сборка, игнорируя кэш
- docker-compose up -d  # Запуск в фоне

Проверьте статус:
- docker-compose ps  # Все сервисы должны быть Up и healthy
- docker-compose logs  # Проверьте логи на ошибки

Примените миграции (если не автоматически):
- docker-compose exec web python manage.py migrate
- docker-compose exec web python manage.py collectstatic --noinput

Создайте суперпользователя:
- docker-compose exec web python manage.py createsuperuser

Откройте приложение:
- Админ-панель: http://localhost/admin/

Для остановки:
- docker-compose down -v (удалит volumes, включая БД).

## Запуск на удаленном сервере:

Адрес развернутого приложения: http://158.160.7.155/

#### Шаги развертывания:

- Подготовьте сервер (VPS, например, на DigitalOcean/AWS с Ubuntu 22.04):
- Обновите систему: sudo apt update && sudo apt upgrade -y.
- Установите Docker и Docker Compose:
- sudo apt install docker.io docker-compose -y
- sudo usermod -aG docker $USER  # Добавьте пользователя в группу docker
- newgrp docker  # Перелогиньтесь
- Установите Git: sudo apt install git -y.

Клонируйте репозиторий на сервер:

- git clone https://github.com/roman/course_project_habit_tracker.git
- cd course_project_habit_tracker

Настройте .env для продакшена:

- DEBUG=False.
- ALLOWED_HOSTS=['localhost', '127.0.0.1', 'web']
- Укажите сильные пароли для БД и SECRET_KEY (генерируйте: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())').
- Для HTTPS: добавьте CSRF_TRUSTED_ORIGINS=https://your-domain.com.

Соберите и запустите:

- docker-compose -f docker-compose.prod.yml build --no-cache  # Если есть отдельный prod-файл; иначе используйте основной
- docker-compose up -d
- docker-compose exec web python manage.py migrate
- docker-compose exec web python manage.py collectstatic --noinput
- docker-compose exec web python manage.py createsuperuser  # Только первый раз
- Настройте автозапуск (systemd):

Создайте сервис /etc/systemd/system/habit-tracker.service:
```
[Unit]
Description=Habit Tracker Docker
Requires=docker.service
After=docker.service

[Service]
WorkingDirectory=/path/to/your/project
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
Restart=always

[Install]
WantedBy=multi-user.target
```

- Активируйте: sudo systemctl daemon-reload && sudo systemctl enable habit-tracker && sudo systemctl start habit-tracker.
- Проверьте: docker-compose ps и логи. Приложение доступно по IP сервера.

- Для обновлений: git pull, затем docker-compose down -v && docker-compose build --no-cache && docker-compose up -d.

## Доступный функционал:

* Вывод списока привычек текущего пользователя с пагинацией.
* Вывод списока публичных привычек.
* Создание привычки.
* Редактирование привычки.
* Удаление привычки.

## Документация:

Для получения дополнительной информации обратитесь к [документации](README.md).