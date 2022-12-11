from datetime import datetime
import pytz
import requests
from celery.signals import worker_ready
from django.conf import settings
from django.core.mail import send_mail
from mailing.celery import app
from .serializers import *


def send_message_service(context, mail, client):
    mail = Mailing.objects.get(pk=mail)
    client = Client.objects.get(pk=client)
    message = Message(status='in process', id_mailing=mail, id_client=client)
    message.save()
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE5Mzc' \
            '5NDIsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Ik5vbnNlbnNlRmFybGllciJ9.syNVHHI-zQx5NqPr1XsERvhBUsuPGxYDcerUmT-v78A'
    req = requests.post(f'https://probe.fbrq.cloud/v1/send/{client.id}',
                        json=context, headers={'Authorization': token}).status_code
    if req == 200:
        message.status = 'ok'
        message.save()
        return 'ok'
    elif req == 400:
        message.status = 'bad'
        message.save()
        return 'bad'
    else:
        message.status = 'error'
        message.save()
        return 'error'


def start_mailing_service(pk):
    mail = Mailing.objects.get(pk=pk)
    time_zone_client = mail.time_zone_client
    code_client = mail.code_client
    if time_zone_client != '0' and code_client:
        clients = Client.objects.filter(code=code_client, time_zone=time_zone_client)
    elif time_zone_client != '0':
        clients = Client.objects.filter(time_zone=time_zone_client)
    elif code_client:
        clients = Client.objects.filter(code=code_client)
    else:
        clients = Client.objects.all()
    for client in clients:
        context = {
            'id': client.id,
            'phone': client.number,
            'text': mail.text
        }
        time_zone = pytz.timezone('Europe/Moscow')
        if mail.time_ended < datetime.now(time_zone):
            return 'overtime'
        send_message.delay(context, mail.id, client.id)
    return 'ok'


def send_stat_every_day_service():
    mailings = Mailing.objects.all().values()
    res = dict()
    for i in mailings:
        messages = list()
        for b in Message.objects.filter(id_mailing=i['id']).order_by('status').values():
            messages += [b]
        res[i['id']] = messages
    res = {'stat': res}
    subject = 'Every day mailing'
    stat = []
    for i in res['stat']:
        content = res['stat'][i]
        s_mes = '\nСообщения:\n'
        for message in content:
            for key in message:
                s_mes += f'     {key}: {message[key]}\n'
        stat.append(f'Айди рассылки {i}: {s_mes}')
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['yarygi66@gmail.com']
    send_mail(subject, '\n'.join(stat), email_from, recipient_list)
    return 'ok'


@app.task
def start_mailing(pk):
    return start_mailing_service(pk)


@app.task
def send_message(context, mail, client):
    return send_message_service(context, mail, client)


@app.task
def send_stat_every_day():
    return send_stat_every_day_service()


@worker_ready.connect
def at_start(sender, **kwargs):
    with sender.app.connection() as conn:
        sender.app.send_task("mailapp.tasks.send_stat_every_day", connection=conn)


