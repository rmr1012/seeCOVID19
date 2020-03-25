from django.db import models

# Create your models here.
class subscriberList(models.Model):
    countryCode=models.CharField(max_length=5)
    province=models.CharField(max_length=20,null=True)
    city=models.CharField(max_length=25,null=True)
    addedTimestamp=models.DateTimeField(auto_now_add=True)
    email=models.CharField(max_length=100)
    name=models.CharField(max_length=100,null=True)

class logFitCache(models.Model):
    countryCode=models.CharField(max_length=5)
    province=models.CharField(max_length=20,null=True)
    city=models.CharField(max_length=25,null=True)
    addedTimestamp=models.DateTimeField(auto_now_add=True)
    email=models.CharField(max_length=100)
    name=models.CharField(max_length=100,null=True)
