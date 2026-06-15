Django Polls

Простое веб-приложение для проведения опросов, написанное на Django.

Возможности
Просмотр списка доступных опросов
Голосование за варианты ответов
Просмотр результатов голосования
Административная панель Django
Хранение данных в PostgreSQL
Деплой на Render
Технологии
Python
Django
PostgreSQL
Gunicorn
Render
Локальный запуск

Клонировать репозиторий:

git clone <repository_url>
cd <repository_name>

Создать и активировать виртуальное окружение:

python -m venv .venv
source .venv/bin/activate

Установить зависимости:

pip install -r requirements.txt

Применить миграции:

python manage.py migrate

Запустить сервер разработки:

python manage.py runserver

Открыть в браузере:

http://127.0.0.1:8000/admin/
Административная панель

Создать суперпользователя:

python manage.py createsuperuser


Автор:
Роман Гугузин