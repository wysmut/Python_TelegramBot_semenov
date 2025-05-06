Проект: Telegram-бот с функцией календаря
Dmitrii Semenov
wysmut
info@dxyzsem.ru

Структура: 
telegram_bot/
├── bot/
│   ├── __init__.py
│   ├── main.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── calendar.py
│   │   ├── common.py
│   │   └── admin.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── calendar_utils.py
│   └── secrets.py
├── django_app/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── app/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_views.py
│   │       └── test_integration.py
└── README.md
