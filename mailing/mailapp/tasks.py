from mailing.celery import app
from mailapp.services import send_message
from .serializers import *


def start_mailing(pk):
    mail = Mailing.objects.get(pk=pk)
    clients = Client.objects.all()
    for client in clients:
        context = {
            'id': client.id,
            'phone': client.number,
            'text': mail.text
        }
        send_mail_message.delay(context, pk, context['id'])
    return 'ok'


@app.task
def start_mailing_off(pk):
    return start_mailing(pk)


@app.task
def send_mail_message(context, mail, client):
    return send_message(context, mail, client)


