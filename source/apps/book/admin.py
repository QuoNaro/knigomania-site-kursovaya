from django.contrib import admin

from .models import Author, Book, Cart, Order, OrderItem


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)  # Поля, отображаемые в списке
    search_fields = ("name",)  # Поля для поиска
    ordering = ("name",)  # Сортировка по имени


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "publisher")  # Поля для отображения
    search_fields = ("title", "author__name")  # Поиск по названию книги и имени автора
    list_filter = ("author", "publisher")  # Фильтры по автору и издателю
    exclude = ("slug",)


class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "quantity", "created_at")  # Поля для отображения
    search_fields = (
        "user__username",
        "book__title",
    )  # Поиск по пользователю и названию книги
    list_filter = ("user",)  # Фильтр по пользователю


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created_at",
        "total_price",
        "arrival_date",
    )  # Поля для отображения
    search_fields = ("user__username",)  # Поиск по пользователю
    list_filter = ("created_at",)  # Фильтр по дате создания


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 1  # Количество пустых форм для добавления новых элементов


# Регистрация моделей с настройками
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Cart, CartAdmin)


# Регистрация OrderItem как Inline в Order
@admin.register(Order)
class OrderWithItemsAdmin(OrderAdmin):
    inlines = [OrderItemAdmin]
