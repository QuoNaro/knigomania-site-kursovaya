from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Описание вашей команды"

    def handle(self, *args, **options):
        self.stdout.write("Ваша команда выполнена успешно")
