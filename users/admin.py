from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser  # Импорт твоей модели


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Поля для отображения в списке пользователей (в таблице админки)
    # Стандартные + твоё кастомное поле
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "telegram_chat_id",  # Твоё поле
        "is_active",
        "is_staff",
        "date_joined",
    )

    # Поля для поиска (можно искать по username, email, имени и т.д.)
    search_fields = ("username", "email", "first_name", "last_name")

    # Фильтры в боковой панели (стандартные для пользователей)
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")

    # Настройки формы редактирования (fieldsets) — разделы для группировки полей
    # Добавляем к стандартным fieldsets (пароль, персональные данные и т.д.) новый раздел
    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {  # Русский заголовок для удобства
                "fields": ("telegram_chat_id",),  # Твоё кастомное поле
                "description": "Поле для интеграции с Telegram-ботом.",
            },
        ),
    )

    # Readonly поля (нельзя редактировать, но видно)
    readonly_fields = ("date_joined",)  # Стандартное поле даты регистрации

    # Сортировка по умолчанию
    ordering = ("username",)

    # Опционально: фильтр по твоему полю, если нужно
    # list_filter += ('telegram_chat_id',)  # Добавит фильтр по telegram_chat_id, если оно не пустое
