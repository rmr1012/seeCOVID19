from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden , HttpResponse
from django.urls import reverse
from seeCOVID19.models import *
from random import *


SITES={}


class HomeView(TemplateView): #some from 48

    template_name = 'seeCOVID19/seeCOVID19.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

@csrf_exempt
def subscribeAPI(request):
    if request.method == 'POST':
        print("got subscrip request")
        email=request.POST.get('email')
        countryCode=request.POST.get('countryCode')
        province=request.POST.get('province')
        city=request.POST.get('city')
        name=request.POST.get('name')
        # print(email,countryCode,province,city,name)
        subscriberList(countryCode=countryCode,province=province,city=city,email=email,name=name).save()

        return HttpResponse(200)
