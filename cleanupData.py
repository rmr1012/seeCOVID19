import json
import simplejson
from datetime import datetime, timezone, timedelta, date
import dateutil.parser
from tqdm import tqdm
import pickle
from lmfit.models import StepModel, LinearModel
import numpy as np
import requests
import pandas as pd
# import matplotlib.pyplot as plt

statesMap = {
'AK': 'Alaska',
'AL': 'Alabama',
'AR': 'Arkansas',
'AS': 'American Samoa',
'AZ': 'Arizona',
'CA': 'California',
'CO': 'Colorado',
'CT': 'Connecticut',
'D.C.': 'District of Columbia',
'DE': 'Delaware',
'FL': 'Florida',
'GA': 'Georgia',
'GU': 'Guam',
'HI': 'Hawaii',
'IA': 'Iowa',
'ID': 'Idaho',
'IL': 'Illinois',
'IN': 'Indiana',
'KS': 'Kansas',
'KY': 'Kentucky',
'LA': 'Louisiana',
'MA': 'Massachusetts',
'MD': 'Maryland',
'ME': 'Maine',
'MI': 'Michigan',
'MN': 'Minnesota',
'MO': 'Missouri',
'MP': 'Northern Mariana Islands',
'MS': 'Mississippi',
'MT': 'Montana',
'NA': 'National',
'NC': 'North Carolina',
'ND': 'North Dakota',
'NE': 'Nebraska',
'NH': 'New Hampshire',
'NJ': 'New Jersey',
'NM': 'New Mexico',
'NV': 'Nevada',
'NY': 'New York',
'OH': 'Ohio',
'OK': 'Oklahoma',
'OR': 'Oregon',
'PA': 'Pennsylvania',
'PR': 'Puerto Rico',
'RI': 'Rhode Island',
'SC': 'South Carolina',
'SD': 'South Dakota',
'TN': 'Tennessee',
'TX': 'Texas',
'UT': 'Utah',
'VA': 'Virginia',
'VI': 'Virgin Islands',
'VT': 'Vermont',
'WA': 'Washington',
'WI': 'Wisconsin',
'WV': 'West Virginia',
'WY': 'Wyoming'
}

def generateMap(data):
    mapObj={}
    countries=set()
    # countriesNeedTally.add("World")
    for item in data["locations"]:
        countries.add(item["country"])

    for country in countries:
        provincesObj={}
        for item in data["locations"]:
            if item["country"]==country and item["province"] != "" and "," not in item["province"]:
                cityList=[]
                for cityItem in data["locations"]:
                    if cityItem["country"]==country and inState(cityItem["province"],item["province"]):
                        cityList.append(cityItem["province"])
                provincesObj[item["province"]]=cityList
        mapObj[country]=provincesObj
    return mapObj
def inState(city,state):

    if "," in city:
        if statesMap[city.split(",")[1].strip()] == state:
            # print(city.split(",")[1].strip(), state)
            return True
    return False
def tallyStates(data,doRecovered=False):
    outData=data
    countryObjs=[]
    seriesID=len(data["locations"])
    for key,state in tqdm(statesMap.items()):
        print("Processing "+state+"\n")
        startDate=datetime.now(timezone.utc)
        endDate=datetime.now(timezone.utc) - timedelta(days=100)
        lastUpdated=datetime.now(timezone.utc) - timedelta(days=100)
        caseTimeSeriesList=pd.Series()
        deathTimeSeriesList=pd.Series()
        recoveredTimeSeriesList=pd.Series()
        countryObj={"province":state}
        country_code=''
        for item in data["locations"]:
            if (data["locations"]["province"]==state and data["locations"]["county"]!=''):
                print(item["province"],item["county"])
                lastUpdated=max(dateutil.parser.parse(item["last_updated"]),lastUpdated)
                caseTimeSeriesList=pd.concat([caseTimeSeriesList, pd.Series(item["timelines"]["confirmed"]["timeline"])], axis=1, sort=False)
                deathTimeSeriesList=pd.concat([deathTimeSeriesList, pd.Series(item["timelines"]["deaths"]["timeline"])], axis=1, sort=False)
                if doRecovered:
                    recoveredTimeSeriesList=pd.concat([recoveredTimeSeriesList, pd.Series(item["timelines"]["recovered"]["timeline"])], axis=1, sort=False)

                country_code=item["country_code"]
                coordinates=item["coordinates"]

        totoalCaseTimeSeries=caseTimeSeriesList.fillna(0).sum(axis=1).to_dict()
        totoalDeathsTimeSeries=deathTimeSeriesList.fillna(0).sum(axis=1).to_dict()
        totoalRecoveredTimeSeries={}
        if doRecovered:
            totoalRecoveredTimeSeries=recoveredTimeSeriesList.fillna(0).sum(axis=1).to_dict()


        dayTotalConfirmed=caseTimeSeriesList.fillna(0).sum(axis=1)[-1]
        dayTotalDeaths=deathTimeSeriesList.fillna(0).sum(axis=1)[-1]
        dayTotalRecovered=0
        if doRecovered:
            dayTotalRecovered=recoveredTimeSeriesList.fillna(0).sum(axis=1)[-1]

        countryObj["country_code"]=country_code
        countryObj["last_updated"]=lastUpdated.isoformat()
        countryObj["coordinates"]=coordinates
        countryObj["province"]=state
        countryObj["id"]=seriesID


        countryObj["latest"]={"confirmed":dayTotalConfirmed,
                    "deaths":dayTotalDeaths,
                    "recovered":dayTotalRecovered
                    }
        countryObj["timelines"]={
            "confirmed": {"latest": dayTotalConfirmed,  "timeline":totoalCaseTimeSeries},
            "deaths":    {"latest": dayTotalDeaths,     "timeline":totoalDeathsTimeSeries},
        }
        if doRecovered:
            countryObj["recovered"]= {"latest": dayTotalRecovered,  "timeline":totoalRecoveredTimeSeries}
        # print(countryObj)
        countryObjs.append(countryObj)
        outData["locations"].append(countryObj)
        seriesID+=1
    return outData,countryObjs

def tallyRegions(data,countriesNeedTally,doRecovered=False):
    outData=data
    countryObjs=[]
    seriesID=len(data["locations"])
    for country in countriesNeedTally:
        print("Processing "+country+"\n")
        startDate=datetime.now(timezone.utc)
        endDate=datetime.now(timezone.utc) - timedelta(days=100)
        lastUpdated=datetime.now(timezone.utc) - timedelta(days=100)
        caseTimeSeriesList=pd.Series()
        deathTimeSeriesList=pd.Series()
        recoveredTimeSeriesList=pd.Series()
        countryObj={"country":country}
        country_code=''
        for item in data["locations"]:
            if (country=="World" and item["province"]=='') or (item["country"] == country and "," not in item["province"]):
                print(item["country"],item["province"])
                lastUpdated=max(dateutil.parser.parse(item["last_updated"]),lastUpdated)
                caseTimeSeriesList=pd.concat([caseTimeSeriesList, pd.Series(item["timelines"]["confirmed"]["timeline"])], axis=1, sort=False)
                deathTimeSeriesList=pd.concat([deathTimeSeriesList, pd.Series(item["timelines"]["deaths"]["timeline"])], axis=1, sort=False)
                if doRecovered:
                    recoveredTimeSeriesList=pd.concat([recoveredTimeSeriesList, pd.Series(item["timelines"]["recovered"]["timeline"])], axis=1, sort=False)

                country_code=item["country_code"]
                coordinates=item["coordinates"]

        totoalCaseTimeSeries=caseTimeSeriesList.fillna(0).sum(axis=1).to_dict()
        totoalDeathsTimeSeries=deathTimeSeriesList.fillna(0).sum(axis=1).to_dict()
        totoalRecoveredTimeSeries={}
        if doRecovered:
            totoalRecoveredTimeSeries=recoveredTimeSeriesList.fillna(0).sum(axis=1).to_dict()


        dayTotalConfirmed=caseTimeSeriesList.fillna(0).sum(axis=1)[-1]
        dayTotalDeaths=deathTimeSeriesList.fillna(0).sum(axis=1)[-1]
        dayTotalRecovered=0
        if doRecovered:
            dayTotalRecovered=recoveredTimeSeriesList.fillna(0).sum(axis=1)[-1]

        if (country=="World"):
            countryObj["country_code"]="WD"
        else:
            countryObj["country_code"]=country_code

        countryObj["last_updated"]=lastUpdated.isoformat()
        countryObj["coordinates"]=coordinates
        countryObj["province"]=""
        countryObj["id"]=seriesID


        countryObj["latest"]={"confirmed":dayTotalConfirmed,
                    "deaths":dayTotalDeaths,
                    "recovered":dayTotalRecovered
                    }
        countryObj["timelines"]={
            "confirmed": {"latest": dayTotalConfirmed,  "timeline":totoalCaseTimeSeries},
            "deaths":    {"latest": dayTotalDeaths,     "timeline":totoalDeathsTimeSeries},
        }
        if doRecovered:
            countryObj["recovered"]= {"latest": dayTotalRecovered,  "timeline":totoalRecoveredTimeSeries}
        # print(countryObj)
        countryObjs.append(countryObj)
        outData["locations"].append(countryObj)
        seriesID+=1
    return outData,countryObjs

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)



if __name__=="__main__":
    # JHUrawData = requests.get("https://coronavirus-tracker-api.herokuapp.com/v2/locations?timelines=1?source=jhu").json()
    CSBSrawData = requests.get("https://coronavirus-tracker-api.herokuapp.com/v2/locations?timelines=1?source=csbs").json()

    outdata,listobj=tallyStates(CSBSrawData)
    print(listobj)
    #
    # outdata,listobj=tallyRegions(rawData,["Canada","China","Australia"])
    # outdata,listobj2=tallyRegions(outdata,["World"])
    # listobj.append(listobj2[0])
    # print(listobj)
    # with open("static/js/seeCOVID19/supplyment.json","w") as outFile:
    #     outFile.write(simplejson.dumps(listobj,ignore_nan=True))



    # with open("static/js/seeCOVID19/map.json","w") as outFile:
    #     outFile.write(simplejson.dumps(mapdata,ignore_nan=True))
