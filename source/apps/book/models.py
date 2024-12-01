import random
from datetime import datetime, timedelta

from django.db import models
from login.models import User
from pytils.translit import slugify as pytils_slugify


class Author(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Имя/Фамилия"
    )  # Уникальное имя автора
    bio = models.TextField(blank=True, verbose_name="Биография")

    class Meta:
        verbose_name = "Автора"
        verbose_name_plural = "Авторы"
        db_table = "author"

    def __str__(self):
        return self.name


class Book(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    genre = models.JSONField(
        null=True, blank=True, verbose_name="Жанры"
    )  # Убедитесь, что это действительно необходимо
    tags = models.JSONField(
        null=True, blank=True, verbose_name="Тэги"
    )  # Убедитесь, что это действительно необходимо
    publisher = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Издательство"
    )
    image = models.URLField(null=True, blank=True, verbose_name="Ссылка на обложку")
    annotation = models.TextField(null=True, blank=True, verbose_name="Описание")
    slug = models.SlugField(unique=True, max_length=255)

    def _generate_unique_slug(self):
        slug = pytils_slugify(self.title)
        unique_slug = slug
        num = 1
        while Book.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.id:  # Проверяем только при создании нового объекта
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Книгу"
        verbose_name_plural = "Книги"
        db_table = "book"

    def __str__(self):
        return f"{self.title} - {self.author}"


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    quantity = models.PositiveBigIntegerField(default=1, verbose_name="Кол-во")
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="Создано"
    )

    class Meta:
        db_table = "cart"
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Корзина"
        unique_together = ("user", "book")  # Уникальность для пользователя и книги


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Общая цена"
    )
    arrival_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата прибытия"
    )
    address = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Адрес доставки"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        db_table = "order"

    def save(self, *args, **kwargs):
        if not self.arrival_date:
            self.arrival_date = self.generate_random_arrival_date()
        super().save(*args, **kwargs)

    def generate_random_arrival_date(self):
        random_days = random.randint(1, 30)
        return datetime.now() + timedelta(days=random_days)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Заказ",
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    quantity = models.PositiveIntegerField(verbose_name="Кол-во")

    class Meta:
        db_table = "order_item"  # Добавьте имя таблицы (если нужно)
