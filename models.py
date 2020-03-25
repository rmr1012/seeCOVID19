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

class mapData(models.Model):
    country=models.CharField(max_length=25,null=False)
    province=models.CharField(max_length=25,null=True)

class locationData(models.Model):
    locationID=models.ForeignKey(mapData,on_delete=models.CASCADE)
    date=models.DateTimeField(null=False)
    count=models.IntegerField(null=False)
    type=models.IntegerField(null=False) # 0 is case 1 is death
    class Meta:
        unique_together = (("locationID","date","type"),)
