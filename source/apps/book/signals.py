from django.db.models.signals import post_migrate
from django.dispatch import receiver

from book.models import Author


@receiver(post_migrate)
def create_default_author(sender, **kwargs):
    # Проверяем, что сигнал относится к нужному приложению
    if sender.name == "book":  # Замените 'book' на имя вашего приложения
        # Создаем автора, если он не существует
        Author.objects.get_or_create(id=999999, defaults={"name": "Автор не указан"})
