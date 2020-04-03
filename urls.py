from django.urls import path, re_path
from seeCOVID19.views import  *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  #as_view is methode in TemplateView
    path(r'subscribe', subscribeAPI, name='subscribeAPI'),  #loading end point, return 1 pair
    path(r'curveFit', curveFitAPI, name='curveFitAPI'),  #loading end point, return 1 pair
    path(r'timeseries', timeseriesAPI, name='timeseriesAPI'),  #loading end point, return 1 pair
    path(r'dailypoll', dailyPollAPI, name='dailyPollAPI'),  #loading end point, return 1 pair
    path(r'map', mapAPI, name='mapAPI'),  #loading end point, return 1 pair
    path(r'dem', demographicsAPI, name='demographicsAPI'),  #loading end point, return 1 pair
]
