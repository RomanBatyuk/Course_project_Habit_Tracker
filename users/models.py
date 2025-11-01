from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Модель пользователя.
    """

    # Дополнительное поле для Telegram Chat ID (для интеграции с ботом)
    telegram_chat_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        unique=True,
        help_text="Telegram Chat ID для отправки напоминаний",
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
