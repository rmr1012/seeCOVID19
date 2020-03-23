from django.contrib import admin

# Register your models here.
from .models import subscriberList

admin.site.register(subscriberList)

class subscriberAdmin(admin.ModelAdmin):
    model = subscriberList
    list_display = ['email', 'country','province', 'city', ]
    list_editable =  ['email', 'country','province', 'city', ]
