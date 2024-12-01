from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from login.models import User

admin.site.site_header = "Книгомания"
admin.site.site_title = "Администратор"
admin.site.index_title = "Добро пожаловать в админ-панель"


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("password", "password2", "username")


class CustomUserAdmin(UserAdmin):
    # Определите поля, которые должны отображаться в списке пользователей в админке
    add_form = CustomUserCreationForm
    list_display = (
        "username",
        "is_superuser",
        "is_staff",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Информация о пользователе", {"fields": ("first_name", "last_name", "group")}),
        ("Разрешения", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": ("username", "password1", "password2"),
            },
        ),
        ("Информация о пользователе", {"fields": ("first_name", "last_name", "group")}),
        ("Разрешения", {"fields": ("is_staff", "is_superuser")}),
    )


# Регистрация модели User
admin.site.register(User, CustomUserAdmin)
# Удаляем модель Group
admin.site.unregister(Group)
