# tz_fb
Техническое задание рассылка

## Зависимосоти: pip install req.txt  
## redis-линукс: 
sudo snap install docker
sudo snap install redis
sudo docker run -d -p 6379:6380 redis
Перейти в mailing cd mailing
№ Запуск сервера: python manage.py runserver
# Запуск celery celery -A mailing worker -l info
# Запуск django-celery_bean celery -A mailing beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
№ Запуск flower: celery -A mailing flower -A mailing --port=5555





