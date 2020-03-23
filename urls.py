from django.urls import path, re_path
from seeCOVID19.views import  *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  #as_view is methode in TemplateView
    path(r'subscribe', subscribeAPI, name='subscribeAPI'),  #loading end point, return 1 pair
]
