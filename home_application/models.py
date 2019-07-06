# -*- coding: utf-8 -*-

from django.db import models


class Host(models.Model):
    name = models.CharField(max_length=30,null=True)
    age = models.CharField(max_length=30,null=True)
    text = models.TextField(null=True)
    when_created = models.CharField(max_length=50,null=True)


class Server(models.Model):
    host = models.ForeignKey(Host)
    background_img = models.BinaryField(null=True)