from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from .tasks import start_mailing


class MailApiCreate(generics.CreateAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingsSerializer

    def post(self, request, *args, **kwargs):
        self.create(request)
        queryset = self.get_queryset()
        mail = MailingsSerializer(queryset, many=True).data[-1]
        start_mailing.apply_async([mail['id']], eta=mail['time_started'])
        return Response({'mail': mail}, status=201)


class ClientApiCreate(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientApiUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingApiUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingsSerializer


class StatApiGlobal(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        mailings = Mailing.objects.all().values()
        stat = dict()
        for i in mailings:
            messages = list()
            for b in Message.objects.filter(id_mailing=i['id']).order_by('status').values():
                messages += [b]
            stat[i['id']] = messages
        return Response({'stat': stat})


class StatApiMailings(generics.ListAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingsSerializer


class StatApiClients(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class StatVApiMessages(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        messages = Message.objects.filter(id_mailing=pk).order_by('status').values()
        return Response({'messages': messages})


class StatApiMessages(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
