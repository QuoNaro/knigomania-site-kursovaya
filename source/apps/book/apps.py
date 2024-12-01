from django.apps import AppConfig


class bookConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "book"
    app_label = "book"
    verbose_name = "Книжный магазин"

    def ready(self):
        pass  # Замените на путь к вашему файлу с сигналами
