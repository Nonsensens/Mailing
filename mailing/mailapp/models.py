from django.db import models


class Mailing(models.Model):
    time_started = models.DateTimeField()
    text = models.TextField(max_length=255)
    code_client = models.IntegerField(max_length=10, default=0)
    time_zone_client = models.CharField(max_length=50, default=0)
    time_ended = models.DateTimeField(default='2012-12-12 12:12:12')
    status = models.BooleanField(default=1)



class Client(models.Model):
    number = models.IntegerField(max_length=10)
    code = models.IntegerField(max_length=10)
    tag = models.CharField(max_length=20)
    time_zone = models.CharField(max_length=50)


class Message(models.Model):
    time_started = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    id_mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)


