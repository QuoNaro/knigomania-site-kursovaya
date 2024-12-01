from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import User


def create_default_admin(sender):
    """Создает учетную запись администратора по умолчанию, если она не существует.

    Проверяет, был ли вызван сигнал от приложения "login". Если учетная запись
    администратора с именем 'admin' отсутствует, создается новая учетная запись
    с заданным именем пользователя и паролем.

    Параметры:
    sender (Model): Модель, отправившая сигнал.
    """
    # Проверяем, что сигнал отправлен от приложения "login"
    if sender.name == "login":

        def check_admin_user() -> bool:
            """Проверяет, существует ли пользователь с именем 'admin'.

            Возвращает True, если пользователь существует, иначе False.

            Возвращает:
            bool: Состояние существования пользователя 'admin'.
            """
            try:
                User.objects.get(username="admin")
                return True
            except Exception:
                return False

        # Если администратора еще нет, создаем его
        if not check_admin_user():
            # Задаем имя пользователя и пароль для администратора
            admin_username = "admin"
            admin_password = "123123"

            # Создаем объект пользователя с правами администратора
            admin_user = User(
                username=admin_username,
                email="admin@example.com",
                is_staff=True,      # Пользователь является сотрудником (имеет доступ к админке)
                is_superuser=True,  # Пользователь имеет все права суперпользователя
            )

            # Устанавливаем пароль для администратора
            admin_user.set_password(admin_password)
            # Сохраняем нового администратора в базе данных
            admin_user.save()


@receiver(post_migrate)
def tasks(sender, **kwargs):
    """Обработчик сигнала post_migrate.

    Вызывается после завершения миграции базы данных.
    Создает учетную запись администратора по умолчанию, если она не существует.

    Параметры:
    sender (Model): Модель, отправившая сигнал.
    kwargs: Дополнительные аргументы, переданные сигналом.
    """
    create_default_admin(sender)
