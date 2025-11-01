from datetime import timedelta

import requests
from celery import shared_task
from django.utils import timezone

from config import settings
from habit.models import Habit

TELEGRAM_API_URL = (
    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
)


@shared_task
def send_habit_reminder(habit_id, chat_id):
    """
    Отложенная задача: отправляет напоминание о выполнении привычки в Telegram.

    habit_id: ID привычки (Habit)
    chat_id: Telegram Chat ID пользователя
    """
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user

        # Проверяем, есть ли chat_id
        if not chat_id:
            print(f"У пользователя {user.username} нет Telegram Chat ID")
            return

        # Формируем сообщение
        message = (
            f"Напоминание о привычке!\n"
            f"Привычка: {habit.name}\n"
            f"Действие: {habit.action}\n"
            f"Место: {habit.place}\n"
            f"Время: {habit.time}\n"
            f"Продолжительность: {habit.duration} сек\n"
            f"Не забудь выполнить!"
        )

        # Отправляем сообщение через Telegram API
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(TELEGRAM_API_URL, json=payload)
        if response.status_code == 200:
            print(f"Напоминание отправлено пользователю {user.username}")
        else:
            print(f"Ошибка отправки: {response.text}")

    except Habit.DoesNotExist:
        print(f"Привычка с ID {habit_id} не найдена")
    except Exception as e:
        print(f"Ошибка в задаче send_habit_reminder: {e}")


@shared_task
def check_and_schedule_reminders():
    """
    Периодическая задача: проверяет все привычки и планирует напоминания на основе periodicity.
    Запускается ежедневно (через Celery Beat).
    """
    now = timezone.now()
    habits = Habit.objects.filter(is_public=False)

    for habit in habits:
        user = habit.user
        chat_id = user.telegram_chat_id if hasattr(user, "telegram_chat_id") else None
        if not chat_id:
            continue

        # Рассчитываем следующее время напоминания
        next_reminder = now.replace(
            hour=habit.time.hour, minute=habit.time.minute, second=0, microsecond=0
        )
        if next_reminder <= now:
            next_reminder += timedelta(days=habit.periodicity)

        # Планируем задачу на next_reminder
        if habit.user.telegram_chat_id:  # Проверка, что chat_id есть
            send_habit_reminder.apply_async(
                args=[habit.id, habit.user.telegram_chat_id]
            )
        else:
            print(
                f"У пользователя {habit.user.username} нет telegram_chat_id, пропускаем напоминание для {habit.name}"
            )

        print(f"Запланировано напоминание для {habit.name} на {next_reminder}")
