from django.db import models


class Mailing(models.Model):
    time_started = models.DateTimeField(null=True)
    text = models.TextField(max_length=255, null=True)
    code_client = models.IntegerField(default=0, null=True)
    time_zone_client = models.CharField(max_length=50, default=0, null=True)
    time_ended = models.DateTimeField(null=True)


class Client(models.Model):
    number = models.IntegerField(null=True)
    code = models.IntegerField(null=True)
    tag = models.CharField(max_length=20, null=True)
    time_zone = models.CharField(max_length=50, null=True)


class Message(models.Model):
    time_started = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    id_mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)


