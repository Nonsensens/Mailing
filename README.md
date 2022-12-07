# Техническое задание рассылка
# Документация:
## Документация по api указана в файле api_docs.txt. Сервис спроектирован при помощи фреймворка django REST. Когда пользователь отправляет запрос на эндпоинт по созданию рассылки, celery и django_celery_bean автоматически принимают эту задачу и выполняют по заданной логике. Функции api доступны. Админка и просмотр с редактированием исполняемых запросов сделаны с помощью flower.
## Доп задачи: 8, 10, 11, 12
## Зависимосоти: pip install req.txt  
## redis-линукс: 
### sudo snap install docker
### sudo snap install redis
### sudo docker run -d -p 6379:6380 redis
## Запуск приложения
### cd mailing
### Запуск сервера: python manage.py runserver
### Запуск celery: celery -A mailing worker -l info
### Запуск django-celery_bean: celery -A mailing beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
### Запуск flower: celery -A mailing flower -A mailing --port=5555





