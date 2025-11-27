from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Habit(models.Model):
    """
    Модель 'Привычка'.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(
        max_length=255, default="Без названия", verbose_name="Название привычки"
    )
    place = models.CharField(max_length=255, help_text="Место, где выполнять привычку")
    time = models.TimeField(
        verbose_name="Время выполнения", help_text="Время выполнения (например, 08:00)"
    )
    duration = models.PositiveIntegerField(
        default=60,
        verbose_name="Продолжительность (секунды)",
        help_text="Не более 120 секунд",
    )
    action = models.CharField(max_length=255, help_text="Описание действия")
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Является ли привычка приятной (вознаграждением)",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        related_name="linked_habits",
        help_text="Связанная приятная привычка (только для полезных)",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (дни)",
        help_text="Не реже 1 раза в 7 дней",
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Вознаграждение",
        help_text="Вознаграждение (если нет связанной привычки)",
    )
    is_public = models.BooleanField(
        default=False, help_text="Публиковать в общий доступ"
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f'{self.name}: {self.action} ({"Приятная" if self.is_pleasant else "Полезная"})'
