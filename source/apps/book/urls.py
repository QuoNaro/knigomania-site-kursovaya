from django.urls import include, path

from . import ajax, views

ajaxpatterns = [
    path("get-money/", ajax.get_money),
    path("load-books/", ajax.load_books),
    path("search/", ajax.search),
    path("add-to-cart/", ajax.add_to_cart),
    path("check-cart/", ajax.check_cart),
    path("get-recommended-books/", ajax.get_recommended_books),
    path("update-address/", ajax.update_address),
    path("place-order/", ajax.place_order),
    path("get-orders/", ajax.get_orders, name="get_orders"),
    path(
        "quantity-minus/",
        ajax.quantity_minus,
    ),
    path(
        "quantity-plus/",
        ajax.quantity_plus,
    ),
    path(
        "remove-cart-item/",
        ajax.remove_cart_item,
    ),
]


urlpatterns = [
    path("", views.home_view, name="home"),
    path("ajax/", include(ajaxpatterns)),
    path("cart/", views.cart_view, name="cart"),
    path("book/<slug:book_slug>/", views.book_view, name="book"),
    path("book/search/<str:query>/", views.search, name="search"),
    path("my/", views.user_view, name="user"),
    path("pay/", views.pay_view, name="pay"),
]
