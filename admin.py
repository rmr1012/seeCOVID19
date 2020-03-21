from django.contrib import admin

# Register your models here.
from .models import QuestionCache

admin.site.register(QuestionCache)

class QuestionAdmin(admin.ModelAdmin):
    model = QuestionCache
    list_display = ['question_id', 'site','added_timestamp', 'query', ]
    list_editable =  ['question_id', 'query', 'content']
