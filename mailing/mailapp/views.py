import datetime

from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .tasks import start_mailing_off


class MailApiStart(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        mail = MailingsSerializer(data=data)
        mail.is_valid(raise_exception=True)
        mail.save()
        start_mailing_off.apply_async([mail.data['id']], eta=mail.data['time_started'])
        mail = Mailing.objects.all()[len(Mailing.objects.all())-1]
        mail.time_ended = datetime.datetime.now()
        mail.save()
        return Response({'mail': model_to_dict(mail)})


class ClientApiList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientApiUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingApiView(generics.ListAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingsSerializer


class MailingApiUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingsSerializer


class StatVApiMessages(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class StatApiGlobal(APIView):
    def get(self, request):
        mailings = Mailing.objects.all().values()
        stat = dict()
        for i in mailings:
            messages = list()
            for b in Message.objects.filter(id_mailing=i['id']).order_by('status').values():
                messages += [b]
            stat[i['id']] = messages
        return Response({'stat': stat})


class StatApiMessages(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        messages = Message.objects.filter(id_mailing=pk).order_by('status').values()
        return Response({'meesages': messages})


