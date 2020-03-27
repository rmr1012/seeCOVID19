from django.db import models

class CompressedTextField(models.TextField):

    def __init__(self, compress_level=6, *args, **kwargs):
        self.compress_level = compress_level
        super(CompressedTextField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(CompressedTextField, self).to_python(value)
        return zlib.compress(value.encode(), self.compress_level)

    def get_prep_value(self, value):
        value = super(CompressedTextField, self).get_prep_value(value)
        return zlib.decompress(value).decode()

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
    country=models.CharField(max_length=40,null=False)
    province=models.CharField(max_length=40,null=True)
    class Meta:
        unique_together = (("country","province"),)

class locationData(models.Model):
    locationID=models.ForeignKey(mapData,on_delete=models.CASCADE)
    date=models.DateTimeField(null=False)
    count=models.IntegerField(null=False)
    type=models.IntegerField(null=False) # 0 is case 1 is death
    class Meta:
        unique_together = (("locationID","date","type"),)
# class mapCache(model.Model):
#     date=models.DateTimeField(null=False,unique=True)
#     mapData = CompressedTextField(null=False)
