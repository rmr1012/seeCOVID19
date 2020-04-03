#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import sys

from io import StringIO

import pandas as pd
from datetime import datetime
import pickle
import numpy as np
# In[2]:


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


# In[3]:

def processCases():
    CSBSrawDataIO = StringIO(requests.get("https://facts.csbs.org/covid-19/covid19_county.csv").text)


    CSBSdf = pd.read_csv(CSBSrawDataIO, sep=",")
    CSBSdf=CSBSdf.rename(columns={"State Name": "Province/State"})

    tstr=CSBSdf["Last Update"][0]
    print(tstr)

    tstr=datetime.strptime(tstr[:-10], '%Y-%m-%d').strftime("%-m/%d/%y")
    print(tstr)


    CSBSStates=CSBSdf.groupby(["Province/State"]).sum().reset_index()
    CSBSStates["Country/Region"]="US"
    CSBSStatesCases=CSBSStates.drop(columns=["New Death","New","Death","Latitude","Longitude"])
    CSBSStatesCases=CSBSStatesCases.rename(columns={"Confirmed": tstr})

    CSBSStatesDeaths=CSBSStates.drop(columns=["New Death","New","Confirmed","Latitude","Longitude"])
    CSBSStatesDeaths=CSBSStatesCases.rename(columns={"Death": tstr})


    CSBSCountydf=CSBSdf.replace({"Province/State":us_state_abbrev})
    CSBSCountydf["Province/State"]=CSBSCountydf["County Name"]+", "+CSBSCountydf["Province/State"]
    CSBSCountydf = CSBSCountydf[~CSBSCountydf['County Name'].isin(['Unassigned'])]
    CSBSCountydf["Country/Region"]="US"

    CSBSCountyCases = CSBSCountydf.drop(columns=["New Death","New","Death","Latitude","Longitude","County Name","Fatality Rate","Last Update"])
    CSBSCountyCases = CSBSCountyCases.rename(columns={"Confirmed": tstr})

    CSBSCountyDeaths = CSBSCountydf.drop(columns=["New Death","New","Confirmed","Latitude","Longitude","County Name","Fatality Rate","Last Update"])
    CSBSCountyDeaths = CSBSCountyDeaths.rename(columns={"Death": tstr})

    legacyJHUCases=StringIO(requests.get("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Confirmed_archived_0325.csv").text)

    legacyJHUCasesdf = pd.read_csv(legacyJHUCases, sep=",")


    newJHUCases=StringIO(requests.get("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv").text)

    newJHUCasesdf = pd.read_csv(newJHUCases, sep=",")

    JHUCasesdf=pd.merge(newJHUCasesdf,legacyJHUCasesdf,how="outer").drop(columns=["Lat","Long"])

    mergeCasesdDF=pd.merge(CSBSStatesCases,JHUCasesdf,how='outer')

    mergeCasesdDF=pd.merge(CSBSCountyCases,mergeCasesdDF,how='outer')

    mergeCasesdDF=mergeCasesdDF.reindex(columnSort(mergeCasesdDF.columns), axis=1)

    mergeCasesdDF["1/22/20"].fillna(0,inplace=True)

    mergeCasesdDF.loc[mergeCasesdDF["Province/State"].isnull() & mergeCasesdDF["Country/Region"].isin(["China"])]

    #find forgotten countries
    forgottenCountriesCases=set(mergeCasesdDF["Country/Region"])-set(mergeCasesdDF[mergeCasesdDF['Province/State'].isnull()]["Country/Region"])

    forgottenCasesDF=mergeCasesdDF.groupby(["Country/Region"]).sum(min_count=1)
    forgottenCasesDF=forgottenCasesDF[forgottenCasesDF.index.isin(forgottenCountriesCases)].reset_index()
    forgottenCasesDF

    fixMergeCasesdDF=pd.merge(forgottenCasesDF,mergeCasesdDF,how='outer')

    fixMergeCasesdDF=fixMergeCasesdDF.reindex(columnSort(fixMergeCasesdDF.columns), axis=1)

    fixMergedDFCasesWorld=fixMergeCasesdDF[fixMergeCasesdDF["Province/State"].isnull()].sum(min_count=1)
    fixMergedDFCasesWorld["Province/State"]=np.NaN
    fixMergedDFCasesWorld["Country/Region"]="World"
    fixMergeCasesdDF=fixMergeCasesdDF.append(fixMergedDFCasesWorld,ignore_index=True)

    pickle.dump( fixMergeCasesdDF, open( "baselineCases0325.dat", "wb" ) )


#--------------------------------------



    legacyJHUDeath=StringIO(requests.get("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Deaths_archived_0325.csv").text)

    legacyJHUDeathdf = pd.read_csv(legacyJHUDeath, sep=",")


    newJHUDeath=StringIO(requests.get("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv").text)

    newJHUDeathdf = pd.read_csv(newJHUDeath, sep=",")

    JHUDeathdf=pd.merge(newJHUDeathdf,legacyJHUDeathdf,how="outer").drop(columns=["Lat","Long"])

    mergeDeathdDF=pd.merge(CSBSStatesDeaths,JHUDeathdf,how='outer')

    mergeDeathdDF=pd.merge(CSBSCountyDeaths,mergeDeathdDF,how='outer')

    mergeDeathdDF=mergeDeathdDF.reindex(columnSort(mergeDeathdDF.columns), axis=1)

    mergeDeathdDF["1/22/20"].fillna(0,inplace=True)

    mergeDeathdDF.loc[mergeDeathdDF["Province/State"].isnull() & mergeDeathdDF["Country/Region"].isin(["China"])]

    #find forgotten countries
    forgottenCountriesDeath=set(mergeDeathdDF["Country/Region"])-set(mergeDeathdDF[mergeDeathdDF['Province/State'].isnull()]["Country/Region"])

    forgottenDeathDF=mergeDeathdDF.groupby(["Country/Region"]).sum(min_count=1)
    forgottenDeathDF=forgottenDeathDF[forgottenDeathDF.index.isin(forgottenCountriesDeath)].reset_index()
    forgottenDeathDF

    fixMergeDeathdDF=pd.merge(forgottenDeathDF,mergeDeathdDF,how='outer')

    fixMergeDeathdDF=fixMergeDeathdDF.reindex(columnSort(fixMergeDeathdDF.columns), axis=1)

    fixMergedDFDeathWorld=fixMergeDeathdDF[fixMergeDeathdDF["Province/State"].isnull()].sum(min_count=1)
    fixMergedDFDeathWorld["Province/State"]=np.NaN
    fixMergedDFDeathWorld["Country/Region"]="World"
    fixMergeDeathdDF=fixMergeDeathdDF.append(fixMergedDFDeathWorld,ignore_index=True)


    pickle.dump( fixMergeDeathdDF, open( "baselineDeath0325.dat", "wb" ) )



    #
def columnSort(columns):
    s=sorted(columns)
    timest=s[:-2]
#     print(s)
    dtl=[]
    for t in timest:
        tt=datetime.strptime(t,'%m/%d/%y')
        dtl.append(tt)

    dtls=sorted(dtl)
    return s[-2:]+list(map(lambda x: x.strftime("%-m/%d/%y"),dtls))


processCases()
