from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden , HttpResponse
from django.urls import reverse
from stackQuiz.models import *
from random import *


SEAPIkey=None
avalSites={"Stack Overflow":"stackoverflow",
"ServerFault":"serverfault",
"Electrical Engineering":"electronics",
"Super User":"superuser",
"Mathematics":"math",
"Ask Ubuntu":"askubuntu"}

SITES={}

try:
    from stackapi import StackAPI
    for siteName,siteHandle in avalSites.items():
        SITES[siteName]=StackAPI(siteHandle,key=SEAPIkey)
        SITES[siteName].max_pages=1
        SITES[siteName].page_size=100
except:
    print("failed to import stackAPI")


class HomeView(TemplateView): #some from 48
    template_name = 'seeCOVID19/seeCOVID19.html'
    def get(self, request):
        return render(request, self.template_name, context)
