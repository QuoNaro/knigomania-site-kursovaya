from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from login.forms import RegisterForm


def login_view(request):
    """Эта функция обрабатывает вход пользователя в систему.

    Если метод запроса POST:
    - Извлекает имя пользователя и пароль из запроса.
    - Использует функцию authenticate Django для проверки учетных данных.
    - Если пользователь аутентифицирован, выполняет вход и перенаправляет на домашнюю страницу.
    - Если аутентификация не удалась, возвращает страницу входа с сообщением об ошибке.

    Если метод запроса GET:
    - Отображает форму входа.

    Параметры:
    request (HttpRequest): Объект запроса Django, содержащий данные запроса.

    Возвращает:
    HttpResponseRedirect: Перенаправление на домашнюю страницу при успешном входе.
    HttpResponse: Страница входа с формой или сообщением об ошибке.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")  # Перенаправьте на вашу домашнюю страницу
        else:
            # Обработка неверных учетных данных
            return render(
                request, "login/login.html", {"error_message": "Invalid login"}
            )
    else:
        return render(request, "login/login.html")


def register_view(request):
    """Обрабатывает регистрацию нового пользователя в системе.

    Если метод запроса POST:
    - Создает экземпляр формы регистрации с данными из запроса.
    - Проверяет валидность формы.
    - Если форма валидна, сохраняет нового пользователя в базе данных, выполняет автоматический вход,
      и перенаправляет на домашнюю страницу.

    Если метод запроса GET:
    - Создает пустую форму регистрации и отображает ее в шаблоне регистрации.

    Параметры:
    request (HttpRequest): Объект запроса Django, содержащий данные запроса.

    Возвращает:
    HttpResponseRedirect: Перенаправление на домашнюю страницу при успешной регистрации.
    HttpResponse: Шаблон регистрации с пустой формой или сообщением об ошибке.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматическая авторизация после регистрации
            return redirect(
                "home"
            )  # Перенаправление на главную страницу или другую после успешной регистрации
    else:
        form = RegisterForm()

    return render(request, "login/register.html", {"form": form})


def logout_view(request):
    """Обрабатывает выход пользователя из системы.

    Эта функция выполняет выход текущего пользователя из системы и
    перенаправляет его на главную страницу.

    Параметры:
    request (HttpRequest): Объект запроса, содержащий информацию о текущем запросе.

    Возвращает:
    HttpResponse: Перенаправление на главную страницу после выхода.

    Примечания:
    - Для корректной работы функции необходимо, чтобы пользователь был
      аутентифицирован перед вызовом этой функции.
    - Функция использует метод `logout` из Django для завершения сессии
      пользователя.
    """
    logout(request)
    return redirect("home")
