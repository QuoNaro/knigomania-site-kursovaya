#!/bin/sh

clear;
if [ "$EUID" -ne 0 ]; then
    echo "Пожалуйста, запустите этот скрипт от имени администратора."
    exit
fi

# Сжимаем директорию в zip-архив
echo "Сжимаем директорию ../d.buzunov/ в архив ../d.buzunov.zip..."
zip -r ../d.buzunov.zip ../d.buzunov/ > /dev/null 2>&1
echo "Сжатие завершено."

# Укажите переменные
USER="root"          # Имя пользователя на удаленном сервере
HOST="192.168.1.234" # IP-адрес или доменное имя удаленного сервера
PASSWORD="182801"    # Ваш пароль
FILE_TO_SEND="../d.buzunov.zip" # Путь к файлу, который нужно отправить
REMOTE_PATH="/root" # Путь на удаленном сервере

# Отправка файла с использованием sshpass
echo "Отправка файла $FILE_TO_SEND на сервер $HOST в директорию $REMOTE_PATH..."
sshpass -p "$PASSWORD" scp -o StrictHostKeyChecking=no "$FILE_TO_SEND" "$USER@$HOST:$REMOTE_PATH"
echo "Файл успешно отправлен."

# Выполнение команд на удаленном сервере
echo "Распаковка архива на удаленном сервере и запуск скрипта build-and-run.sh..."
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USER@$HOST" "unzip '$REMOTE_PATH/d.buzunov.zip' && cd '$REMOTE_PATH/d.buzunov' && sh build-and-run.sh"
echo "Команды выполнены."