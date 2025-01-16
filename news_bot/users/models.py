from django.db import models
from django.utils import timezone

class Persona(models.Model):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    prompt = models.TextField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Photo for {self.name}"
        
class UserProfile(models.Model):
    telegram_id = models.BigIntegerField(unique=True)  # Telegram ID, уникальный для каждого пользователя
    date_birth = models.DateField(null=True, blank=True)  # Дата рождения
    date_death = models.DateField(null=True, blank=True)  # Дата смерти (может быть None, если человек жив)
    short_epigraphy = models.TextField(null=True, blank=True)  # Краткая эпитафия
    is_generated = models.BooleanField(default=False)  # Указывает, сгенерирован ли профиль
    fio = models.CharField(max_length=255, null=True, blank=True)  # Фамилия Имя Отчество
    ready_for_generating = models.BooleanField(default=False) 
    date_joined = models.DateTimeField(default=timezone.now)  # Дата, когда пользователь присоединился
    is_subscribed = models.BooleanField(default=False)  # Статус подписки
    is_admin = models.BooleanField(default=False)  # Статус администратора

    current_persona =  models.ForeignKey(Persona, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"User Profile(telegram_id={self.telegram_id}"

class UserPhoto(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='photos', on_delete=models.CASCADE)  # Связь с UserProfile
    image = models.TextField(null=True, blank=True)  # Путь для хранения изображений

    def __str__(self):
        return f"{self.user_profile.telegram_id}"
