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
import json

import pandas as pd
import requests
import sys

from datetime import datetime,timedelta
from fuzzywuzzy import process
from seeCOVID19.dataProcessor import *

currentMap={"date":datetime.today(),"data":makeMap()}
worldDem= pd.read_csv("seeCOVID19/worldPop.csv", sep=",")
stateDem= pd.read_csv("seeCOVID19/USStatePop.csv", sep=",")
countyDem= pd.read_csv("seeCOVID19/USCountyPop.csv", sep=",")

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

@csrf_exempt
def curveFitAPI(request):
    if request.method == 'POST':
        outdata={}
        jsonData=json.loads(request.body.decode('utf-8'))
        # try:
        print(jsonData["series"])
        outdata=computeRegressionVars(jsonData["series"])
        # except Exception as e:
        #     print(e)
        #     print("unable to fit :(")
        #     outdata=None
        # print(email,countryCode,province,city,name)

        return JsonResponse(outdata)

@csrf_exempt
def mapAPI(request):
    global currentMap
    if request.method == 'GET':

        if currentMap["date"].date()==datetime.today().date():
            outMap=currentMap["data"]
            print("sending old map!")
        else:
            print("Making New Map!",currentMap["date"].strftime("%m-%d-%Y"),datetime.today().strftime("%m-%d-%Y"))
            newMap=makeMap()
            currentMap={"date":datetime.today(),"data":newMap}
            outMap=newMap
        return JsonResponse(outMap)


@csrf_exempt
def timeseriesAPI(request):
    if request.method == 'GET':
        id=int(request.GET["id"])
        mapdata=mapData.objects.get(id=id)
        country=mapdata.country
        if mapdata.province == "nan":
            province=""
        else:
            province=mapdata.province
        casesList=list(locationData.objects.filter(locationID=id,type=0).values())
        casesList=sorted(casesList,key= lambda x : x["date"].isoformat())

        deathsList=list(locationData.objects.filter(locationID=id,type=1).values())
        deathsList=sorted(deathsList,key= lambda x : x["date"].isoformat())

        recoveredList=list(locationData.objects.filter(locationID=id,type=2).values())
        recoveredList=sorted(recoveredList,key= lambda x : x["date"].isoformat())

        last_updated=casesList[-1]["date"].isoformat()
        latest_confirmed=casesList[-1]["count"]
        latest_deaths=deathsList[-1]["count"]
        latest_recovered=0

        latest_recovered=recoveredList[-1]["count"]
        recoveredList=list(locationData.objects.filter(locationID=id,type=2).values())

        casesDict = { i["date"].isoformat() : i["count"] for i in casesList }
        deathsDict = { i["date"].isoformat() : i["count"] for i in deathsList }
        recoveredDict = { i["date"].isoformat() : i["count"] for i in recoveredList }
        return JsonResponse({"country":country,"province":province,"last_updated":last_updated ,
                            "latest":{"confirmed":latest_confirmed,"deaths":latest_deaths,"recovered":latest_recovered},
                            "confirmed":casesDict,"deaths":deathsDict,"recovered":recoveredDict})
@csrf_exempt
def demographicsAPI(request):
    if request.method == 'GET':
        country=request.GET.get('country')
        state=request.GET.get('state')
        county=request.GET.get('county')
        print(country,state,county)

        if county != "":
            print("county detected!")
            myStateDem=countyDem[countyDem["state"]==state]
            options=list(myStateDem["county"])
            rowID = options.index(process.extractOne(county,options)[0])
            print(rowID,myStateDem.iloc[rowID,:])
            row=myStateDem.iloc[rowID,:]
            pop=int(row["pop"])
            density=int(row["density"])
            # row=
        elif state != "":
            row=stateDem[stateDem["state"]==state]
            print("state detected")
            pop=int(row["pop"])
            density=int(row["density"])
        else:
            print("country detected")
            row=worldDem[worldDem["country"]==country]
            pop=int(row["pop"])
            density=int(row["density"])
        return JsonResponse({"pop":pop,"density":density})

@csrf_exempt
def dailyPollAPI(request):
    if request.method == 'GET':
        count=storeTodayData()
        count1=storeYesterdayData()
        return JsonResponse({"count":count+count1})
