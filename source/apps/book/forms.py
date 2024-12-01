# forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

from .models import User


class UserChangeForm(BaseUserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "address", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Дополнительные настройки формы (например, добавление классов CSS)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)  # Устанавливаем новый пароль, если он указан
        if commit:
            user.save()
        return user
