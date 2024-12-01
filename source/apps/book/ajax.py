import json

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from book.models import Book, Cart, Order, OrderItem


@login_required
def get_money(request: HttpRequest):
    if request.method == "GET":
        money = request.GET.get("money", 0)
        request.user.money += int(money)
        request.user.save()
        return JsonResponse({"status": "Access"})
    return JsonResponse({"status": "Invalid"})


@require_GET
def load_books(request: HttpRequest):
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 10))

    items = Book.objects.select_related("author")

    if (max_price := request.GET.get("price")) and max_price != "None":
        items = items.filter(price__lt=int(max_price))

    if (a := request.GET.get("author_id")) and a != "None":
        author_ids = request.GET.getlist("author_id")[0].split(",")
        author_query = Q()
        for author_id in author_ids:
            author_query |= Q(author_id=author_id)
        items = items.filter(author_query)

    if (g := request.GET.get("genre")) and g != "None":
        genres = g.split(",")
        genre_query = Q()
        for genre in genres:
            genre_query |= Q(genre__icontains=genre)
        items = items.filter(genre_query)

    if (t := request.GET.get("tag")) and t != "None":
        tags = t.split(",")
        tag_query = Q()
        for tag in tags:
            tag_query |= Q(tags__icontains=tag)
        items = items.filter(tag_query)

    items = items[offset : offset + limit]

    data = [
        {
            "id": book.id,
            "title": book.title,
            "author_name": book.author.name,
            "price": book.price,
            "genre": book.genre,
            "tags": book.tags,
            "publisher": book.publisher,
            "image": book.image,
            "annotation": book.annotation,
            "slug": book.slug,
        }
        for book in items
    ]

    return JsonResponse(
        {"items": data, "has_more": Book.objects.count() > offset + limit},
        encoder=DjangoJSONEncoder,
    )


def truncate_string(str, max_length=30):
    if len(str) > max_length:
        # Обрезаем строку до последнего пробела перед max_length
        trimmed = str[:max_length]
        if str[max_length : max_length + 1] != " ":
            trimmed = trimmed[: trimmed.rfind(" ")]
        return trimmed + "..."  # Добавляем многоточие
    return str  # Возвращаем строку без изменений, если она короче max_length


@require_GET
def search(request):
    try:
        query = request.GET.get("query", "")
        items = Book.objects.select_related("author").filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )

        books_list = []
        for item in items:
            short_title = truncate_string(item.title, max_length=60)
            books_list.append(
                {
                    "id": item.id,
                    "price": item.price,
                    "title": item.title,
                    "short_title": short_title,
                    "author_name": item.author.name,
                    "genre": item.genre,
                    "tags": item.tags,
                    "publisher": item.publisher,
                    "image": item.image,
                    "annotation": item.annotation,
                    "slug": item.slug,
                }
            )
        return JsonResponse({"status": "Access", "books": books_list[:5]})
    except Exception as e:
        return JsonResponse({"status": "Invalid", "error": str(e)})


@require_POST
@login_required
def check_cart(request: HttpRequest):
    quantity = 0
    book_id = int(request.POST.get("book_id"))
    cart_items = Cart.objects.all().filter(user_id=request.user.id)
    cart_ids_items = [i.book_id for i in cart_items]

    if book_id in cart_ids_items:
        quantity = cart_items.get(book_id=book_id).quantity

    return JsonResponse({"status": "Access", "quantity": quantity})


@require_POST
@login_required
def add_to_cart(request: HttpRequest):
    try:
        book_id = int(request.POST.get("book_id"))
        book = get_object_or_404(Book, pk=book_id)

        # Используем update_or_create для обработки существующих записей
        cart_item, created = Cart.objects.update_or_create(
            user=request.user,
            book=book,
        )

        if not created:
            # Если запись была обновлена, увеличиваем количество
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse(
            {
                "status": "success",
                "data": {"book_id": cart_item.book.id, "quantity": cart_item.quantity},
            }
        )

    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)}, status=400)


def get_recommended_books_list(book_id):
    book = Book.objects.get(pk=book_id)

    tag_query = Q()
    for tag in book.tags:
        tag_query |= Q(tags__icontains=tag)

    genre_query = Q()
    for genre in book.genre:
        genre_query |= Q(genre__icontains=genre)

    recommended_books = Book.objects.filter(genre_query | tag_query).exclude(id=book.pk)

    recommended_books_random = list(recommended_books.order_by("?")[:5].values())

    for b in recommended_books_random:
        b["short_title"] = truncate_string(b["title"], max_length=30)

    return recommended_books_random


@require_GET
def get_recommended_books(request: HttpRequest):
    print("Hello")
    book_id = request.GET.get("book_id")
    r_books = get_recommended_books_list(book_id)
    return JsonResponse({"status": "Success", "data": r_books})


@require_POST
@login_required
def update_address(request: HttpRequest):
    try:
        address = request.POST.get("address")

        request.user.address = address
        request.user.save()
        return JsonResponse({"status": "Success"})
    except Exception as e:
        return JsonResponse({"status": "Error", "error": str(e)}, status=400)


@login_required
@require_POST
def place_order(request: HttpRequest):
    items = request.POST.get("items")
    items = json.loads(items)
    total_price = sum(i["price"] for i in items)
    request.user.money -= total_price
    request.user.save()

    # Создаём заявку
    order, is_created = Order.objects.get_or_create(
        user=request.user,
        total_price=total_price,
        address=request.POST.get("address").strip(),
    )

    # Создаём OrderItem для каждого товара в заявке
    for item in items:
        book_id = item["book_id"]
        quantity = item["quantity"]

        # Проверка наличия книги
        if not Book.objects.filter(pk=book_id).exists():
            continue  # Можно добавить логику обработки ошибки

        # Создание OrderItem
        order_item, created = OrderItem.objects.get_or_create(
            order=order, book_id=book_id, defaults={"quantity": quantity}
        )
        print(created)

        # Удаление элемента из корзины
        try:
            cart_item = Cart.objects.get(book_id=book_id)
            cart_item.delete()
        except Cart.DoesNotExist as e:
            print(f"Error while deleting cart item: {str(e)}")
            continue  # Или обработайте ошибку, если элемент не найден

    return JsonResponse({"status": "success"})


@login_required
def get_orders(request):
    # Получаем все заказы пользователя с предзагрузкой предметов заказа
    orders = Order.objects.filter(user=request.user).prefetch_related("order_items")

    order_list = []
    for order in orders:
        order_items = [
            {
                "book_id": item.book.id,
                "title": item.book.title,
                "quantity": item.quantity,
            }
            for item in order.order_items.all()
        ]
        order_list.append(
            {
                "order_id": order.id,
                "arrival_date": order.arrival_date,
                "address": order.address,
                "total_price": str(order.total_price),  # Приводим к строке для JSON
                "items": order_items,
            }
        )

    return JsonResponse({"status": "success", "orders": order_list})


@login_required
@require_POST
def quantity_minus(request):
    cart_item_id = request.POST.get("cart_item_id")
    cart_object = Cart.objects.get(pk=cart_item_id)
    cart_object.quantity -= 1
    cart_object.save()
    return JsonResponse({"status": "success"})


@login_required
@require_POST
def quantity_plus(request):
    cart_item_id = request.POST.get("cart_item_id")
    cart_object = Cart.objects.get(pk=cart_item_id)
    cart_object.quantity += 1

    cart_object.save()
    return JsonResponse({"status": "success"})


@login_required
@require_POST
def remove_cart_item(request):
    cart_item_id = request.POST.get("cart_item_id")
    print(cart_item_id)
    cart_object = Cart.objects.get(pk=cart_item_id)
    cart_object.delete()
    return JsonResponse({"status": "success"})
