# Стадия 1: Сборка библиотек
FROM python:3.11-slim AS builder

WORKDIR /app

# Сначала копируем только список зависимостей ради кэширования слоёв
COPY requirements.txt .

# Устанавливаем зависимости в изолированный каталог /install
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Стадия 2: Финальный легковесный образ
FROM python:3.11-slim

WORKDIR /app

# Переносим из стадии builder только скомпилированные пакеты
COPY --from=builder /install /usr/local

# Копируем остальной исходный код приложения
COPY . .

# Точка входа: боевой запуск Flask через WSGI-сервер Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]









Было:

# Делаем Дебиан и Пайтон
FROM python:3.11-slim

# Рабочая среда
WORKDIR /app

# Копируем в рабочую среду
COPY . /app

# Установка зависимостей
RUN pip install -r requirements.txt 

# Выполнить команду
CMD ["python", "main.py"]