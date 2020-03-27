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
from lmfit.models import StepModel, LinearModel
from lmfit import Parameters, fit_report, minimize

from scipy import interpolate
import math
import pandas as pd
import pytz
from django.forms.models import model_to_dict
import requests
import sys

from io import StringIO

from datetime import datetime,timedelta
import pickle


SITES={}

forgottenCountries=["China","Canada","Australia","Cruise Ship"]
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'US Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

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
        try:
            locationID=mapData.objects.filter(country=country,province=province)[0]
        except IndexError:
            mapData(country=country,province=province).save()
            locationID=mapData.objects.filter(country=country,province=province)[0]
        cleanrow=row.drop(["Country/Region","Province/State"])
        for key, value in cleanrow.items():
            if value is not None:
                if not math.isnan(value):
                    # print(key)
                    try:
                        obj, created = locationData.objects.update_or_create(
                            locationID=locationID, type=0,date=datetime.strptime(key,'%m/%d/%y'),
                            defaults={'count': value},
                        )
                        # locationData(locationID=locationID,date=datetime.strptime(key,'%m/%d/%y'),count=value,type=0).save()
                    except Exception as e:
                        print(str(e))
                        print(locationID,locationID.country,locationID.province)
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def retraceDailyData():
    day0=datetime.strptime("2020-01-22", '%Y-%m-%d').date()
    today=datetime.today().date()
    for day in daterange(day0, today):
        storeDayData(day)

def storeTodayData():
    today=datetime.today()
    return storeDayData(today)

def storeDayData(day):
    dayDF=makeDayDF(day)
    index=0
    if dayDF is not None:
        for index,row in tqdm(dayDF.iterrows()):
            country=row["Country/Region"]
            province=row["Province/State"]
            cases=row["Confirmed"]
            deaths=row["Deaths"]
            recovered=row["Recovered"]
            try:
                locationID=mapData.objects.filter(country=country,province=province)[0]
            except IndexError:
                mapData(country=country,province=province).save()
                locationID=mapData.objects.filter(country=country,province=province)[0]
            # print(locationID,locationID.country,locationID.province)
            # print(country,province,cases,deaths,recovered)
            if cases is not None:
                if not math.isnan(cases):
                    # print(key)
                    try:
                        obj, created = locationData.objects.update_or_create(
                            locationID=locationID, type=0,date=day,
                            defaults={'count': cases},
                        )
                        # locationData(locationID=locationID,date=datetime.strptime(key,'%m/%d/%y'),count=value,type=0).save()
                    except Exception as e:
                        print(str(e))
                        print(locationID,locationID.country,locationID.province)
            if deaths is not None:
                if not math.isnan(deaths):
                    # print(key)
                    try:
                        obj, created = locationData.objects.update_or_create(
                            locationID=locationID, type=1,date=day,
                            defaults={'count': deaths},
                        )
                        # locationData(locationID=locationID,date=datetime.strptime(key,'%m/%d/%y'),count=value,type=0).save()
                    except Exception as e:
                        print(str(e))
                        print(locationID,locationID.country,locationID.province)
            if recovered is not None:
                if not math.isnan(recovered):
                    # print(key)
                    try:
                        obj, created = locationData.objects.update_or_create(
                            locationID=locationID, type=2,date=day,
                            defaults={'count': recovered},
                        )
                        # locationData(locationID=locationID,date=datetime.strptime(key,'%m/%d/%y'),count=value,type=0).save()
                    except Exception as e:
                        print(str(e))
                        print(locationID,locationID.country,locationID.province)

    return index
def makeMap():
    dat=list(mapData.objects.all().values())
    df=pd.DataFrame(dat,dtype=int)
    outObj={}
    for country, df_region in df.groupby("country"):
        countryList=df_region[df_region["province"].isin(["nan"])]
        # print("haha",country)
        if len(countryList["id"].values)>0:
            countryID=countryList["id"].values[0]

            provinceList=df_region[~df_region["province"].str.contains(",") & ~df_region["province"].isin(["nan"])]

            provinceDict={}
            for index,province in provinceList.iterrows():
                    casesList=list(locationData.objects.filter(locationID=province["id"],type=0).values())
                    try:
                        latest_confirmed=casesList[-1]["count"]
                    except:
                        print(countryID,country,casesList)
                        latest_confirmed=0
                    provinceDict[province["province"]]={"id":int(province["id"]),"cities":{},"cases":latest_confirmed}
            if country == "US":
                countyList=df_region[df_region["province"].str.contains(",")]
                countyList[["county","province"]]=countyList["province"].str.split(",",expand=True)
                countyList["province"]=countyList["province"].str.strip()
                us_state_abbrev_rev = {value:key for key, value in us_state_abbrev.items()}
                countyList=countyList.replace({"province":us_state_abbrev_rev})
                # print(countyList)
                for state, df_state in countyList.groupby("province"):
                    countyDict={}
                    for index,county in df_state.iterrows():
                        countyDict[county["county"]]=int(county["id"])
                    # print(countyDict)
                    try:
                        provinceDict[county["province"]]["cities"]=countyDict
                    except:
                        print("coun't build map for ",county["province"])
            # print(country,countryID)
            casesList=list(locationData.objects.filter(locationID=countryID,type=0).values())
            try:
                latest_confirmed=casesList[-1]["count"]
            except:
                print(countryID,country,casesList)
                latest_confirmed=0
            outObj[country]={"id":int(countryID),"provinces":provinceDict,"cases":latest_confirmed}

    return outObj

def makeDayDF(day):
    url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+day.strftime("%m-%d-%Y")+".csv"
    print(url)
    response=requests.get(url)
    if response.status_code == 200:
        JHUDailyst = StringIO(response.text)

        JHUDailyDf = pd.read_csv(JHUDailyst, sep=",")
        try:
            JHUDailyDf=JHUDailyDf.rename(columns={"Province_State":"Province/State","Country_Region":"Country/Region","Last_Update":"Last Update"})
        except:
            print("no need to translate")

        tstr=JHUDailyDf["Last Update"][0]
        print(tstr)
        tstr=dateutil.parser.parse(tstr).strftime("%-m/%d/%y")

        JHUDailyDf=JHUDailyDf.replace({"Country/Region":{"Mainland China":"China","Hong Kong":"China","Macau":"China"}})

        JHUDailyStateDf=JHUDailyDf[JHUDailyDf["Country/Region"].isin(["US"])].groupby(["Province/State"]).sum().reset_index()
        JHUDailyStateDf["Country/Region"]="US"
        JHUDailyStateDf

        if 'Admin2' in JHUDailyDf:
            JHUDailyDfUS=JHUDailyDf[JHUDailyDf["Country/Region"]=="US"]
            JHUDailyDfUS=JHUDailyDfUS.replace({"Province/State":us_state_abbrev})
            JHUDailyDfUS["Province/State"]=(JHUDailyDfUS["Admin2"]+", "+JHUDailyDfUS["Province/State"]).fillna("N/A")

            JHUDailyDfNotUS=JHUDailyDf[JHUDailyDf["Country/Region"]!="US"]

            JHUDailyDfTran=pd.concat([JHUDailyDfUS,JHUDailyDfNotUS])
            JHUDailyDfTran=JHUDailyDfTran.drop(columns=["Admin2","Last Update","FIPS"])
        else:
            JHUDailyDfTran=JHUDailyDf

        forgottenCountries=set(JHUDailyDfTran["Country/Region"])-set(JHUDailyDfTran[JHUDailyDfTran['Province/State'].isnull()]["Country/Region"])

        forgottenDF=JHUDailyDfTran.groupby(["Country/Region"]).sum(min_count=1)
        forgottenDF=forgottenDF[forgottenDF.index.isin(forgottenCountries)].reset_index()

        fixMergeDF=pd.merge(forgottenDF,JHUDailyDfTran,how='outer')
        fixMergeWorld=fixMergeDF[fixMergeDF["Province/State"].isnull()].sum()
        fixMergeWorld["Province/State"]=np.NaN
        fixMergeWorld["Country/Region"]="World"
        fixMergeDF=fixMergeDF.append(fixMergeWorld,ignore_index=True)

        fixMergeStateDF=pd.merge(fixMergeDF,JHUDailyStateDf,how='outer')
        fixMergeStateDF
        return fixMergeStateDF
    return None

def updateBaseLineDeathsData():
    df = pickle.load( open( "baselineDeath0325.dat", "rb" ) )
    for index,row in tqdm(df.iterrows()):
        # if index==0:
        country=row["Country/Region"]
        province=row["Province/State"]
        try:
            locationID=mapData.objects.filter(country=country,province=province)[0]
        except IndexError:
            mapData(country=country,province=province).save()
            locationID=mapData.objects.filter(country=country,province=province)[0]
        cleanrow=row.drop(["Country/Region","Province/State"])
        for key, value in cleanrow.items():
            if value is not None:
                if not math.isnan(value):
                    # print(key)
                    try:
                        # locationData(locationID=locationID,date=datetime.strptime(key,'%m/%d/%y'),count=value,type=1).save()
                        obj, created = locationData.objects.update_or_create(
                            locationID=locationID, type=1,date=datetime.strptime(key,'%m/%d/%y'),
                            defaults={'count': value},
                        )
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
    if request.method == 'GET':
        return JsonResponse(makeMap())


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
def dailyPollAPI(request):
    if request.method == 'GET':
        count=storeTodayData()
        return JsonResponse({"count":count})



def computeRegressionVars(timeseries):
    timeseries=sorted(timeseries,key=lambda srs: srs["t"])
    y=np.array([val["y"] for val in timeseries],dtype=np.uint32)
    t=np.array([val["t"] for val in timeseries],dtype=np.uint64)/1000/24/3600

    print(y)
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

    for sig in [0.1,7,.5,4,2]:
        pars = model.make_params(line_intercept=ydata.min(),
                                 line_slope=0,
                                 step_center=xdata.mean(),
                                 step_amplitude=ydata.std(),
                                 step_sigma=sig)
        # fit data to this model with these parameters
        try:
            print("Fitting curve...")
            out = model.fit(ydata, pars, x=xdata)
            print("curve fitted!")
        except Exception as e:
            print(e)
            print("Fit exception hit, retrying with other inits")
        #composite_err=(out.params["step_sigma"].stderr/out.params["step_sigma"].value)+(out.params["step_center"].stderr/out.params["step_center"].value)+(out.params["step_amplitude"].stderr/out.params["step_amplitude"].value)
        #print("composite error = ",composite_err)
        if out.params["step_sigma"].value >0 and out.params["step_sigma"].value <30:
           break

    print(fit_report(out))
    amplitudeErr=(out.params["step_amplitude"].stderr/out.params["step_amplitude"].value)
    amplitude=out.params["step_amplitude"].value
    centerErr=(out.params["step_center"].stderr/out.params["step_center"].value)
    center=out.params["step_center"].value
    sigmaErr=(out.params["step_sigma"].stderr/out.params["step_sigma"].value)
    sigma=out.params["step_sigma"].value


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
