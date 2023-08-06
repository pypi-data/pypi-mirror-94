=====
django-pass-code
=====

Приложение для авторизации через смс, при помощи сервиса smsc.ru


Быстрый запуск
-----------

1. Добавьте "account" в файле settings.py в INSTALLED_APPS::

    INSTALLED_APPS = [
        ...
        'account',
    ]

2. Подключите путь account::

    path('account/', include('account.urls')),

3. Выполните ``python manage.py migrate`` для миграций.