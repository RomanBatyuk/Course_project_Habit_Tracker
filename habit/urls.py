from django.urls import path

from habit.apps import HabitConfig
from habit.views import (
    HabitCreateAPIView,
    HabitDestroyAPIView,
    HabitListAPIView,
    HabitPublicListAPIView,
    HabitUpdateAPIView,
)

app_name = HabitConfig.name


urlpatterns = [
    path("create/", HabitCreateAPIView.as_view(), name="create"),
    path("ListPaginate/", HabitListAPIView.as_view(), name="ListPaginate"),
    path("ListPublic/", HabitPublicListAPIView.as_view(), name="ListPublic"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(), name="update"),
    path("delete/<int:pk>/", HabitDestroyAPIView.as_view(), name="delete"),
]
