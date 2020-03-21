from django.urls import path, re_path
from stackQuiz.views import  *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  #as_view is methode in TemplateView
    path('load', LoadAPI, name='loadAPI'),  #loading end point, return 1 pair
    path('search', SearchAPI, name='searchAPI'), #loading end point, return 3 pair
    # path('fetch', FetchAPI, name='home'), #loading end point, return 3 pair
]
