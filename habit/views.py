from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.paginators import PaginationList
from habit.serializers import CreateHabitSerializer, HabitSerializer


class HabitListAPIView(ListAPIView):
    """
    Контроллер для вывода списка привычек текущего пользователя с пагинацией.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationList

    def get_queryset(self):
        """
        Фильтруем привычки только текущего пользователя.
        """
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.none()
        user = self.request.user
        return Habit.objects.filter(user=user)


class HabitPublicListAPIView(ListAPIView):
    """
    Контроллер для вывода списка публичных привычек текущего пользователя.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Фильтруем публичные привычки только текущего пользователя.
        """
        return Habit.objects.filter(is_public=True)


class HabitCreateAPIView(CreateAPIView):
    """
    Контроллер создания привычки.
    """

    queryset = Habit.objects.all()
    serializer_class = CreateHabitSerializer
    permission_classes = [IsAuthenticated]


class HabitUpdateAPIView(UpdateAPIView):
    """
    Контроллер для редактирования привычки.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Фильтруем привычки только текущего пользователя.
        """
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.none()
        user = self.request.user
        return Habit.objects.filter(user=user)


class HabitDestroyAPIView(DestroyAPIView):
    """
    Контроллер для удаления привычки.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Фильтруем привычки только текущего пользователя.
        """
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.none()
        user = self.request.user
        return Habit.objects.filter(user=user)
