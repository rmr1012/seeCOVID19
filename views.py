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
import numpy as np
import dateutil.parser
from tqdm import tqdm
import pickle
from lmfit.models import StepModel, LinearModel
from lmfit import Parameters, fit_report, minimize

import numpy as np
from scipy import interpolate
import math
import pandas as pd
from datetime import datetime
import pytz
SITES={}

forgottenCountries=["China","Canada","Australia","Cruise Ship"]


def updateMap():
    df = pickle.load( open( "baseline0325.dat", "rb" ) )
    for index,row in df.iterrows():
        print(row["Country/Region"],row["Province/State"])
        try:
            mapData(country=row["Country/Region"],province=row["Province/State"]).save()
        except Exception as e:
            print(str(e))

def updateBaseLineCasesData():
    df = pickle.load( open( "baselineCases0325.dat", "rb" ) )
    for index,row in tqdm(df.iterrows()):
        # if index==0:
        country=row["Country/Region"]
        province=row["Province/State"]
        locationID=mapData.objects.filter(country=country,province=province)[0]
        cleanrow=row.drop(["Country/Region","Province/State"])
        for key, value in cleanrow.items():
            if not math.isnan(value):
                # print(key)
                try:
                    locationData(locationID=locationID,date=datetime.strptime(key,'%m/%d/%y'),count=value,type=0).save()
                except Exception as e:
                    print(str(e))
                    print(locationID,locationID.country,locationID.province)

def updateBaseLineDeathsData():
    df = pickle.load( open( "baselineDeaths0325.dat", "rb" ) )
    for index,row in tqdm(df.iterrows()):
        # if index==0:
        country=row["Country/Region"]
        province=row["Province/State"]
        locationID=mapData.objects.filter(country=country,province=province)[0]
        cleanrow=row.drop(["Country/Region","Province/State"])
        for key, value in cleanrow.items():
            if not math.isnan(value):
                # print(key)
                try:
                    locationData(locationID=locationID,date=datetime.strptime(key,'%m/%d/%y'),count=value,type=1).save()
                except Exception as e:
                    print(str(e))
                    print(locationID,locationID.country,locationID.province)




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
        jsonData=json.loads(request.body)
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
def supplymentAPI(request):
    if request.method == 'POST':
        country=request.POST.get('country')
        data=json.loads("static/js/seeCOVID19/"+country+".js")
        return JsonResponse(data)

@csrf_exempt
def logCountyAPI(request):
    if request.method == 'POST':
        country=request.POST.get('country')
        data=json.loads("static/js/seeCOVID19/"+country+".js")
        return JsonResponse(data)


def computeRegressionVars(timeseries):
    y=np.array([val["y"] for val in timeseries],dtype=np.uint32)
    t=np.array([val["t"] for val in timeseries],dtype=np.uint64)/1000/24/3600
    day0=t[0]
    t=t-t[0]
    dayz=t[-1]
    print("Days detected",dayz)

    f = interpolate.interp1d(t, y)

    xdata=np.arange(0,dayz,1,dtype=np.uint16)
    ydata=f(xdata)
    print(xdata)
    print(ydata)
    # model data as Step + Line
    step_mod = StepModel(form='logistic', prefix='step_')
    model = step_mod
    # make named parameters, giving initial values:

    for sig in [0.1,5,.5,3,2]:
        pars = model.make_params(line_intercept=ydata.min(),
                                 line_slope=0,
                                 step_center=xdata.mean(),
                                 step_amplitude=ydata.std(),
                                 step_sigma=sig)
        # fit data to this model with these parameters
        out = model.fit(ydata, pars, x=xdata)
        print(out.params["step_sigma"].value)
        if out.params["step_sigma"].value >0:
            break

    print(fit_report(out))
    relativeErrors=[]
    values=[]

    for name, param in out.params.items():
        values.append(param.value)
        try:
            relativeErrors.append(100*param.stderr/param.value)
        except:
            relativeErrors.append(None)
    amplitudeErr=relativeErrors[0]
    amplitude=values[0]
    centerErr=relativeErrors[1]
    center=values[1]
    sigmaErr=relativeErrors[2]
    sigma=values[2]


    # print("Time Series Day 0",day0)
    # print("Projected Total Cases",amplitude)
    # print("Projected Turning Point",center)
    # print("Projected Sigma",sigma)
    return {"day0":day0*1000*24*3600,
            "amplitude":amplitude,
            "amplitud_err":amplitudeErr,
            "center":center,
            "center_err":centerErr,
            "sigma":sigma,
            "sigma_err":sigmaErr}
