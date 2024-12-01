from django.contrib.auth.management.commands import createsuperuser


class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        options.setdefault("email", None)  # Установите значение None для email
        return super().handle(*args, **options)
