import requests
from .serializers import *


def send_message(context, pk, client):
    mail = Mailing.objects.get(pk=pk)
    client = Client.objects.get(pk=client)
    message = Message(status='in process', id_mailing=mail, id_client=client)
    message.save()
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE5Mzc5NDIsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Ik5vbnNlbnNlRmFybGllciJ9.syNVHHI-zQx5NqPr1XsERvhBUsuPGxYDcerUmT-v78A'
    req = requests.post(f'https://probe.fbrq.cloud/v1/send/{client.id}', json=context, headers={'Authorization': token}).status_code
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
