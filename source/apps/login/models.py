from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, password, **extra_fields):
        """ """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(username, password, **extra_fields)

    def _create_user(self, username, password, **extra_fields):
        """Создает и возвращает пользователя с указанным email и паролем."""
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    class Meta:
        db_table = "User"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"
        app_label = "login"

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    money = models.IntegerField(default=0)
    start_bonus = models.BooleanField(default=False)
    address = models.CharField(default="")
