from django.db import models

# Create your models here.
class QuestionCache(models.Model):
    question_id=models.CharField(max_length=15)
    site=models.CharField(max_length=55)
    added_timestamp=models.DateTimeField(auto_now_add=True,null=True)
    query=models.CharField(max_length=100)
    content=models.CharField(max_length=6536,null=True) ## raw api response item
