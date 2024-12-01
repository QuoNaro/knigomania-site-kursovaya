#!/bin/sh

clear;
if [ "$EUID" -ne 0 ]; then
    echo "Пожалуйста, запустите этот скрипт от имени администратора."
    exit
fi
docker-compose down;


# Функция для установки Python и pip
install_python_and_pip() {
    echo "Установка Python и pip..."

    # Проверка наличия Python
    if command -v python3 >/dev/null 2>&1; then
        echo "Python уже установлен."
    else
        # Установка Python и pip в зависимости от пакетного менеджера
        if command -v apt >/dev/null 2>&1; then
            sudo apt update
            sudo apt install -y python3 python3-pip
        elif command -v yum >/dev/null 2>&1; then
            sudo yum install -y python3 python3-pip
        elif command -v apk >/dev/null 2>&1; then
            sudo apk update
            sudo apk add --no-cache python3 py3-pip  # Установка py3-pip для Alpine
            ln -sf python3 /usr/bin/python  # Создание символической ссылки для удобства
        else
            echo "Неизвестный пакетный менеджер. Установка не выполнена."
            exit 1
        fi
    fi

    # Установка пакетов через pip
    echo "Установка пакетов через pip..."

    # Список пакетов для установки
    packages="django psycopg2-binary"  # Замените на нужные вам пакеты

    for package in $packages; do
        pip3 install "$package" --break-system-packages
    done

    echo "Все пакеты установлены."
}

# Проверка наличия пакетного менеджера и вызов функции установки
if command -v apt >/dev/null 2>&1; then
    echo "Обнаружен пакетный менеджер APT."
    install_python_and_pip
elif command -v yum >/dev/null 2>&1; then
    echo "Обнаружен пакетный менеджер YUM."
    install_python_and_pip
elif command -v apk >/dev/null 2>&1; then
    echo "Обнаружен пакетный менеджер APK."
    install_python_and_pip
else
    echo "Пакетный менеджер не найден. Убедитесь, что вы используете Debian/Ubuntu, CentOS/RHEL или Alpine."
    exit 1
fi



echo "Вход в .venv"
source .venv/bin/activate
echo "Отчистка существующих статических файлов перед началом"
rm -rf './source/static'
echo "Сбор статических файлов..."
python source/manage.py collectstatic
echo "Отчистка существующих статических файлов"
rm -rf './volumes/static'
echo "Перенос статических файлов в volume"
mv -f "source/static" "./volumes/static"

echo "Запуск контейнеров"
docker-compose up -d --build
