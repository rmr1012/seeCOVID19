import json
import simplejson
from datetime import datetime, timezone, timedelta, date
import dateutil.parser
from tqdm import tqdm
import pickle
from lmfit.models import StepModel, LinearModel
import numpy as np
import requests
# import matplotlib.pyplot as plt

def cleanupData(data):
    regionMapObj={}
    countriesNeedTally=set()
    # countriesNeedTally.add("World")
    for item in data["locations"]:
        # print(item["country"])
        if item["province"] != "":
            countriesNeedTally.add(item["country"])
            # print(item["province"])
        if (item["country"] in countriesNeedTally) and item["province"] == "":
            countriesNeedTally.remove(item["country"])

    # for country in countriesNeedTally:


    # pickle.dump( outdata1, open( "wip.dat", "wb" ) )
    #
    # outdata1 = pickle.load( open( "wip.dat", "rb" ) )

    mapObj=generateMap(outdata1)
    outdata2=tallyRegions(outdata1,["World"])

    outdata2["map"]=mapObj
    return outdata2

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
    if "," in city:
        if statesMap[city.split(",")[1].strip()] == state:
            # print(city.split(",")[1].strip(), state)
            return True
    return False

def tallyRegions(data,countriesNeedTally,doRecovered=False):
    outData=data
    countryObjs=[]
    seriesID=len(data["locations"])
    for country in countriesNeedTally:
        print("Processing "+country+"\n")
        startDate=datetime.now(timezone.utc)
        endDate=datetime.now(timezone.utc) - timedelta(days=100)
        lastUpdated=datetime.now(timezone.utc) - timedelta(days=100)
        caseTimeSeriesList=[]
        deathTimeSeriesList=[]
        recoveredTimeSeriesList=[]
        countryObj={"country":country}
        country_code=''
        for item in data["locations"]:
            if (country=="World" and item["province"]=='') or (item["country"] == country and "," not in item["province"]):
                print(item["country"],item["province"])
                caseTimeSeriesList.append(item["timelines"]["confirmed"]["timeline"])
                startDate=min(dateutil.parser.parse(list(item["timelines"]["confirmed"]["timeline"].keys())[0]),startDate)
                endDate=max(dateutil.parser.parse(list(item["timelines"]["confirmed"]["timeline"].keys())[-1]),endDate)
                lastUpdated=max(dateutil.parser.parse(item["last_updated"]),lastUpdated)

                deathTimeSeriesList.append(item["timelines"]["deaths"]["timeline"])
                startDate=min(dateutil.parser.parse(list(item["timelines"]["deaths"]["timeline"].keys())[0]),startDate)
                endDate=max(dateutil.parser.parse(list(item["timelines"]["deaths"]["timeline"].keys())[-1]),endDate)
                lastUpdated=max(dateutil.parser.parse(item["last_updated"]),lastUpdated)

                if doRecovered:
                    recoveredTimeSeriesList.append(item["timelines"]["recovered"]["timeline"])
                    startDate=min(dateutil.parser.parse(list(item["timelines"]["recovered"]["timeline"].keys())[0]),startDate)
                    endDate=max(dateutil.parser.parse(list(item["timelines"]["recovered"]["timeline"].keys())[-1]),endDate)
                    lastUpdated=max(dateutil.parser.parse(item["last_updated"]),lastUpdated)

                country_code=item["country_code"]
                coordinates=item["coordinates"]

        if (country=="World"):
            countryObj["country_code"]="WD"
        else:
            countryObj["country_code"]=country_code

        countryObj["last_updated"]=lastUpdated.isoformat()
        countryObj["coordinates"]=coordinates
        countryObj["province"]=""
        countryObj["id"]=seriesID


        print(startDate,endDate)
        totoalCaseTimeSeries={}
        totoalDeathsTimeSeries={}
        totoalRecoveredTimeSeries={}
        dayTotalRecovered=0
        dayTotalConfirmed=0
        dayTotalDeaths=0
        for single_date in tqdm(daterange(startDate, endDate),total=(endDate-startDate).days):
            # print(single_date.strftime("%Y-%m-%d"))
            dayTotalConfirmed=0
            for regionList in caseTimeSeriesList:
                for dateStr,count in regionList.items():
                    if dateutil.parser.parse(dateStr).date() == single_date.date():
                        dayTotalConfirmed+=count
            totoalCaseTimeSeries[single_date.isoformat()]=dayTotalConfirmed

            dayTotalDeaths=0
            for regionList in deathTimeSeriesList:
                for dateStr,count in regionList.items():
                    if dateutil.parser.parse(dateStr).date() == single_date.date():
                        dayTotalDeaths+=count
            totoalDeathsTimeSeries[single_date.isoformat()]=dayTotalDeaths
            if doRecovered:
                dayTotalRecovered=0
                for regionList in recoveredTimeSeriesList:
                    for dateStr,count in regionList.items():
                        if dateutil.parser.parse(dateStr).date() == single_date.date():
                            dayTotalRecovered+=count
                totoalRecoveredTimeSeries[single_date.isoformat()]=dayTotalRecovered

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

def injectRegressions(data):
    outdata=data
    for index,location in enumerate(data["locations"]):
        for key,value in location["timelines"].items():
            outdata["locations"][index]["timelines"][key]["logistic_fit"]={}
            outdata["locations"][index]["timelines"][key]["logistic_fit"]["fitted"]=False


    for sigma_init in [0.5,1,2,5]:
        for index,location in tqdm(enumerate(data["locations"]),total=len(data["locations"])):
            # print(location["country"],location["province"])
            for key,value in location["timelines"].items():
                day0=None
                amplitude=None
                center=None
                sigma=None
                try:
                    if not outdata["locations"][index]["timelines"][key]["logistic_fit"]["fitted"]:
                        valObj = computeRegressionVars(value["timeline"],step_sigma=sigma_init)
                        outdata["locations"][index]["timelines"][key]["logistic_fit"]["fitted"]=True
                        outdata["locations"][index]["timelines"][key]["logistic_fit"]["values"]=valObj
                except Exception as e:
                    pass
                    # print(str(e),location["country"],location["province"])
                    # print("unable to fit")
                # print(day0, amplitude, center, sigma)

    failcount=0

    for index,location in enumerate(data["locations"]):
        for key,value in location["timelines"].items():
            if outdata["locations"][index]["timelines"][key]["logistic_fit"]["fitted"] == False:
                failcount+=1

    print(failcount,"/",len(data["locations"])*3,"failed")
    return outdata
    # day0, amplitude, center, sigma = computeRegressionVars(data["locations"][1]["timelines"]["confirmed"]["timeline"])
    # print(day0, amplitude, center, sigma)
def injectLogSlope(data):
    outdata=data
    for index,location in tqdm(enumerate(data["locations"]),total=len(data["locations"])):
        for key,value in location["timelines"].items():
            day0=dateutil.parser.parse(list(value["timeline"].keys())[1])
            valArr=np.array(list(value["timeline"].values()))
            logValArr=np.log10(valArr)
            logDiffVar=np.diff(logValArr)

            concavityObj={}
            for val in logDiffVar:
                concavityObj[day0.isoformat()]=val
                day0=day0+timedelta(days=1)
            outdata["locations"][index]["timelines"][key]["log_slope_timeline"]=concavityObj
    return outdata

def injectLogConcavity(data):
    outdata=data
    for index,location in tqdm(enumerate(data["locations"]),total=len(data["locations"])):
        for key,value in location["timelines"].items():
            day0=dateutil.parser.parse(list(value["timeline"].keys())[2])
            valArr=np.array(list(value["timeline"].values()))
            logValArr=np.log10(valArr)
            logDiffVar=np.diff(np.diff(logValArr))

            concavityObj={}
            for val in logDiffVar:
                concavityObj[day0.isoformat()]=val
                day0=day0+timedelta(days=1)
            outdata["locations"][index]["timelines"][key]["log_concavity_timeline"]=concavityObj
    return outdata


def computeRegressionVars(timeseries,step_sigma=2):
    y=list(timeseries.values())
    tslen=len(y)
    x=range(tslen)

    xdata=np.array(x)
    ydata=np.array(y)
    # model data as Step + Line
    step_mod = StepModel(form='logistic', prefix='step_')
    model = step_mod
    # make named parameters, giving initial values:
    pars = model.make_params(line_intercept=ydata.min(),
                             line_slope=0,
                             step_center=xdata.mean(),
                             step_amplitude=ydata.std(),
                             step_sigma=step_sigma)
    # fit data to this model with these parameters
    out = model.fit(ydata, pars, x=xdata)

    relativeErrors=[]
    values=[]
    for name, param in out.params.items():
        values.append(param.value)
        relativeErrors.append(100*param.stderr/param.value)
    amplitudeErr=relativeErrors[0]
    amplitude=values[0]
    centerErr=relativeErrors[1]
    center=values[1]
    sigmaErr=relativeErrors[2]
    sigma=values[2]

    day0=list(timeseries.keys())[0]
    # print("Time Series Day 0",day0)
    # print("Projected Total Cases",amplitude)
    # print("Projected Turning Point",center)
    # print("Projected Sigma",sigma)
    return {"day0":day0,
            "amplitude":amplitude,
            "amplitud_err":amplitudeErr,
            "center":center,
            "center_err":centerErr,
            "sigma":sigma,
            "sigma_err":sigmaErr}



if __name__=="__main__":
    APIurl="https://coronavirus-tracker-api.herokuapp.com/v2/locations?timelines=1"
    response= requests.get(APIurl)
    rawData = response.json()
    # print("Downloaded latest dataset")
    # # rawData=json.loads(open("static/js/seeCOVID19/clean.json","r").read())
    # with open("static/js/seeCOVID19/raw.json","w") as outFile:
    #     outFile.write(json.dumps(rawData))
    #     print("written raw.json")
    # rawData=json.loads(open("static/js/seeCOVID19/processed.json","r").read())
    # mapdata=generateMap(rawData)
    # pickle.dump( rawData, open( "wip1.dat", "wb" ))
    # cleanData=cleanupData(rawData)
    # pickle.dump( cleanData, open( "wip2.dat", "wb" ))
    # injectedData=injectRegressions(cleanData)
    # pickle.dump( injectedData, open( "wip3.dat", "wb" ))
    # # rawData=json.loads(open("static/js/seeCOVID19/processed.json","r").read())
    # concavLogData=injectLogConcavity(injectedData)
    # pickle.dump( concavLogData, open( "wip4.dat", "wb" ))
    # # concavLogData = pickle.load( open( "wip3.dat", "rb" ) )
    # slopeLogData=injectLogSlope(concavLogData)
    outdata,listobj=tallyRegions(rawData,["Canada","China","Australia"])
    outdata,listobj2=tallyRegions(outdata,["World"])
    listobj.append(listobj2[0])
    print(listobj)
    with open("static/js/seeCOVID19/supplyment.json","w") as outFile:
        outFile.write(simplejson.dumps(listobj,ignore_nan=True))
    # with open("static/js/seeCOVID19/map.json","w") as outFile:
    #     outFile.write(simplejson.dumps(mapdata,ignore_nan=True))
