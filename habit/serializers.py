from rest_framework import serializers

from habit.models import Habit


class CreateHabitSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для создания привычки.
    """

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):
        """
        Валидация данных перед созданием экземпляра.
        """
        periodicity = data.get("periodicity")
        duration = data.get("duration")
        is_pleasant = data.get("is_pleasant")
        reward = data.get("reward")
        related_habit = data.get("related_habit")

        # Проверка periodicity
        if periodicity is not None and periodicity not in range(1, 8):
            raise serializers.ValidationError(
                {"periodicity": "Периодичность должна быть от 1 до 7 дней."}
            )

        # Проверка duration
        if duration is not None and duration > 120:
            raise serializers.ValidationError(
                {
                    "duration": "Продолжительность выполнения привычки не должна превышать 120 секунд."
                }
            )

        # Проверка связей для приятной привычки
        if is_pleasant:
            if reward is not None:
                raise serializers.ValidationError(
                    {"reward": "У приятной привычки не может быть вознаграждения."}
                )
            if related_habit is not None:
                raise serializers.ValidationError(
                    {
                        "related_habit": "У приятной привычки не может быть связанной привычки."
                    }
                )
        else:
            # Для полезной привычки: должен быть reward ИЛИ related_habit, но не оба и не ни одного
            if reward is None and related_habit is None:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": "Для полезной привычки укажите вознаграждение"
                                            "или связанную приятную привычку."
                    }
                )
            if reward is not None and related_habit is not None:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": "Для полезной привычки укажите либо вознаграждение,"
                                            "либо связанную приятную привычку, но не оба."
                    }
                )

        # Проверка related_habit: она должна быть приятной
        if related_habit is not None:
            if not related_habit.is_pleasant:
                raise serializers.ValidationError(
                    {"related_habit": "Связанная привычка должна быть приятной."}
                )

        return data

    def create(self, validated_data):
        # Присваиваем текущего пользователя
        validated_data["user"] = self.context["request"].user
        # Создаём и сохраняем экземпляр (валидация уже прошла в validate())
        instance = Habit(**validated_data)
        instance.save()
        return instance


class HabitSerializer(serializers.ModelSerializer):
    """
    Универсальный сериалайзер для модели Habit.
    """

    class Meta:
        model = Habit
        fields = "__all__"
