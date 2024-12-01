from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.login.urls")),  # Авторизация
    path("", include("apps.book.urls")),
]
