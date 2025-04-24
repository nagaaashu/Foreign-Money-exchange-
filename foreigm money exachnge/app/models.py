from django.db import models

class Users(models.Model):
    fname=models.CharField(default="",max_length=1000)
    email=models.CharField(default="",max_length=1000)
    password=models.CharField(default="",max_length=1000)
    uname=models.CharField(default="",max_length=1000)
    checkPoint=models.CharField(default="",max_length=1000)
    balance=models.IntegerField(default=0)
    curr=models.CharField(default="",max_length=1000)
    id=models.IntegerField(auto_created=True,primary_key=True,unique=True)

class CurrencyRate(models.Model):
    exRate=models.CharField(default="",max_length=1000)
    name=models.CharField(default="",max_length=10000)
    id=models.IntegerField(auto_created=True,primary_key=True,unique=True)