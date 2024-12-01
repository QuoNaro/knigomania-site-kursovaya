import itertools

from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET
from login.models import User

from book.models import Author, Book, Cart

from .ajax import truncate_string


def home_view(request: HttpRequest):
    if request.user.is_authenticated and not request.user.start_bonus:
        user = User.objects.get(pk=request.user.id)
        user.start_bonus = True
        user.money += 1500
        user.save()
        # Обновляем объект пользователя в текущей сессии
        request.user = user

    Book.objects.all()
    all_genres = [i["genre"] for i in list(Book.objects.values("genre"))]
    all_genres = list(set(itertools.chain.from_iterable(all_genres)))

    all_tags = [i["tags"] for i in list(Book.objects.values("tags"))]
    all_tags = list(set(itertools.chain.from_iterable(all_tags)))

    all_authors = list(Author.objects.all().values())
    return render(
        request,
        "book/home.html",
        {"authors": all_authors, "genres": all_genres, "tags": all_tags},
    )


def book_view(request, book_slug: str):
    # Получаем книгу и преобразуем в словарь

    book = Book.objects.get(slug=book_slug)
    cart = Cart.objects.all().filter(user_id=request.user.id)
    cart_ids = [i.book_id for i in cart]

    context = {
        "book": book,
        "cart_ids": cart_ids,
        "cart": cart,
    }

    return render(request, "book/book.html", context)


def truncate_string(str, max_length=30):
    if len(str) > max_length:
        # Обрезаем строку до последнего пробела перед max_length
        trimmed = str[:max_length]
        if str[max_length : max_length + 1] != " ":
            trimmed = trimmed[: trimmed.rfind(" ")]
        return trimmed + "..."  # Добавляем многоточие
    return str  # Возвращаем строку без изменений, если она короче max_length


@require_GET
def search(request, query: str):
    items = Book.objects.select_related("author").filter(
        Q(title__icontains=query) | Q(author__name__icontains=query)
    )

    # Формируем список книг с именем автора
    books_list = []
    for item in items:
        short_title = truncate_string(item.title, max_length=30)
        books_list.append(
            {
                "id": item.id,
                "price": item.price,
                "title": item.title,
                "short_title": short_title,
                "author_name": item.author.name,  # Используем имя автора
                "genre": item.genre,
                "tags": item.tags,
                "publisher": item.publisher,
                "image": item.image,
                "annotation": item.annotation,
                "slug": item.slug,
            }
        )

    return render(request, "book/search.html", {"books": books_list})


def pay_view(request: HttpRequest):
    return render(request, "book/maintence.html")


def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user).order_by("-created_at")
    total_price = sum(item.book.price * item.quantity for item in cart_items)

    for item in cart_items:
        item.total_price = item.quantity * item.book.price  # Рассчитываем общую цену
    # for i in cart_items :
    #     i.book.short_title = truncate_string(i.book.title, max_length=30)

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "book/cart.html", context)


def user_view(request: HttpRequest):
    return render(request, "book/maintence.html")
