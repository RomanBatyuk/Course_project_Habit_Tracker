# from rest_framework import serializers
# from django.contrib.auth import get_user_model
#
# User = get_user_model()  # Если используешь CustomUser, замени на него
#
#
# class CustomUserSerializer(serializers.ModelSerializer):
#     """
#     Сериалайзер для создания пользователя.
#     """
#
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password', 'is_active')
#         extra_kwargs = {
#             'is_active': {'read_only': True},
#         }
#
#     def create(self, validated_data):
#         # Извлекаем пароль из validated_data
#         password = validated_data.pop('password')
#
#         # Создаём объект пользователя
#         user = User(**validated_data)
#
#         # Хэшируем пароль
#         user.set_password(password)
#
#         # Сохраняем в БД
#         user.save()
#
#         return user
