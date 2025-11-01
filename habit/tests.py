import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from habit.models import Habit


User = get_user_model()


class HabitAPITestCase(APITestCase):
    """
    Тестовый случай для API эндпоинтов привычек.
    Тестируем CRUD операции, публичные привычки, аутентификацию, валидацию и пагинацию.
    Используем аутентифицированного клиента и тестовые привычки.
    """

    def setUp(self):
        """
        Настройка тестовых фикстур.
        Создаем тестового пользователя, аутентифицируем его
        и создаем тестовые привычки (приватные, приятные и публичные).
        """
        # Создаём тестового пользователя
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        # Создаём токен для аутентификации
        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # Создаём привычки для тестов
        self.habit1 = Habit.objects.create(
            user=self.user,
            name="Пить воду",
            place="Кухня",
            time="08:00:00",
            duration=120,
            action="Выпить стакан воды",
            is_pleasant=False,
            periodicity=1,
            reward="Чувствовать себя бодрым",
            is_public=False,
        )
        self.habit2 = Habit.objects.create(
            user=self.user,
            name="Зарядка",
            place="Комната",
            time="07:00:00",
            duration=60,
            action="Сделать 10 отжиманий",
            is_pleasant=True,
            periodicity=2,
            reward=None,
            is_public=True,
        )
        self.public_habit = Habit.objects.create(
            user=self.user,
            name="Публичная привычка",
            place="Парк",
            time="10:00:00",
            duration=90,
            action="Прогулка",
            is_pleasant=True,
            periodicity=1,
            reward=None,
            is_public=True,
        )

    def test_habit_list(self):
        """
        Тестирование списка всех привычек для аутентифицированного пользователя.
        Проверяет статус 200 и правильное количество результатов.
        """
        url = reverse("habit:ListPaginate")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 3)

    def test_habit_create(self):
        """
        Тестирование создания новой привычки.
        Сначала пытается с недопустимой длительностью (>120), ожидая 400,
        затем с валидными данными, ожидая 201 и увеличенное количество объектов.
        """
        url = reverse("habit:create")
        data = {
            "name": "Читать книгу",
            "place": "Кресло",
            "time": "20:00:00",
            "duration": 180,
            "action": "Прочитать 10 страниц",
            "is_pleasant": False,
            "periodicity": 3,
            "reward": "Узнать новое",
            "is_public": False,
        }
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)  # duration > 120
        data["duration"] = 120
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 4)

    def test_habit_update(self):
        """
        Тестирование обновления существующей привычки через PATCH.
        Проверяет статус 200 и что имя привычки обновлено.
        """
        url = reverse("habit:update", kwargs={"pk": self.habit1.pk})
        data = {
            "name": "Пить чай",
            "place": "Кухня",
            "time": "09:00:00",
            "duration": 60,
            "action": "Выпить чашку чая",
            "is_pleasant": False,
            "periodicity": 1,
            "reward": "Расслабиться",
            "is_public": False,
            "related_habit": None,
        }
        response = self.client.patch(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.habit1.refresh_from_db()
        self.assertEqual(self.habit1.name, "Пить чай")

    def test_habit_delete(self):
        """
        Тестирование удаления существующей привычки.
        Проверяет статус 204 и уменьшение количества объектов.
        """
        url = reverse("habit:delete", kwargs={"pk": self.habit1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Habit.objects.count(), 2)

    def test_habit_list_public(self):
        """
        Тестирование списка публичных привычек.
        Проверяет статус 200 и правильное количество публичных привычек.
        """
        url = reverse("habit:ListPublic")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_unauthenticated_access(self):
        """
        Тестирование доступа к эндпоинту создания без аутентификации.
        Проверяет статус 401 для неавторизованного POST запроса.
        """
        self.client.credentials()
        url = reverse("habit:create")
        data = {
            "name": "Тест",
            "place": "Тест",
            "time": "10:00:00",
            "duration": 60,
            "action": "Тест",
            "periodicity": 1,
        }
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_create_invalid_periodicity(self):
        """
        Тестирование создания привычки с недопустимой периодичностью (>7).
        Проверяет статус 400 из-за ошибки валидации.
        """
        url = reverse("habit:create")
        data = {
            "name": "Тест",
            "place": "Тест",
            "time": "10:00:00",
            "duration": 60,
            "action": "Тест",
            "is_pleasant": False,
            "periodicity": 10,  # >7
            "reward": "Тест",
            "is_public": False,
        }
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_duration(self):
        """
        Тестирование создания привычки с недопустимой длительностью (>120).
        Проверяет статус 400 из-за ошибки валидации.
        """
        url = reverse("habit:create")
        data = {
            "name": "Тест",
            "place": "Тест",
            "time": "10:00:00",
            "duration": 150,  # >120
            "action": "Тест",
            "is_pleasant": False,
            "periodicity": 1,
            "reward": "Тест",
            "is_public": False,
        }
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_pleasant_with_reward(self):
        """
        Тестирование создания приятной привычки с вознаграждением (недопустимая комбинация).
        Проверяет статус 400 из-за валидации в методе clean().
        """
        url = reverse("habit:create")
        data = {
            "name": "Тест",
            "place": "Тест",
            "time": "10:00:00",
            "duration": 60,
            "action": "Тест",
            "is_pleasant": True,
            "periodicity": 1,
            "reward": "Не должно быть",
            "is_public": False,
        }
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_pleasant_without_reward(self):
        """
        Тестирование создания приятной привычки без вознаграждения.
        Проверяет статус 201 для успешного создания.
        """
        url = reverse("habit:create")
        data = {
            "name": "Тест",
            "place": "Тест",
            "time": "10:00:00",
            "duration": 60,
            "action": "Тест",
            "is_pleasant": True,
            "periodicity": 1,
            "reward": None,
            "is_public": False,
        }
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_pagination(self):
        """
        Тестирование пагинации в списке привычек.
        Создает дополнительные привычки и проверяет, что страница 2 возвращает 5 привычек.
        """
        for i in range(10):
            Habit.objects.create(
                user=self.user,
                name=f"Привычка {i}",
                place="Тест",
                time="10:00:00",
                duration=60,
                action=f"Действие {i}",
                periodicity=1,
                is_public=False,
            )
        url = reverse("habit:ListPaginate")
        response = self.client.get(url, {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 5)

    def test_partial_update(self):
        """
        Тестирование частичного обновления привычки (только поле name).
        Проверяет статус 200 и что обновлено только указанное поле.
        """
        url = reverse("habit:update", kwargs={"pk": self.habit1.pk})
        data = {"name": "Обновлено"}
        response = self.client.patch(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.habit1.refresh_from_db()
        self.assertEqual(self.habit1.name, "Обновлено")
