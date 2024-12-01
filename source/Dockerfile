# Базовый образ с Python
FROM python:3.12.7-alpine

# Установка зависимостей для сборки
RUN apk update && apk upgrade

# Устанавливаем рабочую директорию
WORKDIR /app/

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app/

# Запуск Gunicorn
ENTRYPOINT ["/app/docker-entrypoint.sh"]