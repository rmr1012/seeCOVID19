statesDict = {
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
};

var isoCountries = {
        'Cruise Ship': 'XX',
        'Australia': 'AU',
        'Canada': 'CA',
        'China': 'CN',
        'United States': 'US',
    };

var rawData
var currentID=0;
var forgottenCountries=[]
function simpleConfig(label)
{
  return {
    // The type of chart we want to create
    type: 'line',
    // The data for our dataset
    data: {
        datasets: [
          {
            label: 'Fitted Logistic Curve',
            fill:false,
            borderDash:[5,5],
            backgroundColor: 'rgb(50, 50, 230)',
            borderColor: 'rgb(50, 50, 230)',

          },{
          label: 'Recorded Data',
          backgroundColor: 'rgb(255, 99, 132)',
          borderColor: 'rgb(255, 99, 132)',

        },  ]
    },

    // Configuration options go here
    options: {
      responsive: true,
      maintainAspectRatio:false,
      // aspectRatio:1.6,
      title: {
        display: true,
      },
      legend:{
        display: true
      },
      scales: {
        xAxes: [{
          type: 'time',
          time: {
                  displayFormats: {
                      quarter: 'MMM DD'
                  }
              },
          distribution: 'linear',
          offset: true,
          ticks: {
            source: 'auto',
          },

        }],
        yAxes: [{
          gridLines: {
            drawBorder: false
          },
          scaleLabel: {
            display: true,
            labelString: label
          }
        }]
      },
    }
}
}
function derivativeConfig(label){
  return {
    type: 'line',
    data: {
        datasets: [
          {
            label: label,
            fill:false,
            backgroundColor: 'rgb(50, 50, 230)',
            borderColor: 'rgb(50, 50, 230)',
          }]
    },
    options: {
      responsive: true,
      maintainAspectRatio:false,
      // aspectRatio:1.6,
      title: {
        display: true,
      },
      legend:{
        display: true
      },
      scales: {
        xAxes: [{
          type: 'time',
          time: {
                  displayFormats: {
                      quarter: 'MMM DD'
                  }
              },
          distribution: 'linear',
          offset: true,
          ticks: {
            source: 'auto',
          },

        }],
        yAxes: [{
          gridLines: {
            drawBorder: false
          },
          scaleLabel: {
            display: true,
            labelString: label
          }
        }]
      },
    }
  }
}
function logTicker(...args) {
   const value = Chart.Ticks.formatters.logarithmic.call(this, ...args);
   // console.log(value)
   if (value.length) {
     return Number(value).toLocaleString()
   }
   return value;
 }

var casesLinChart = new Chart($('#canvas-cases-linear')[0].getContext('2d'), simpleConfig('Comfirmed Cases'));
var casesLogChart = new Chart($('#canvas-cases-log')[0].getContext('2d'), simpleConfig('Comfirmed Cases'));
casesLogChart.options.scales.yAxes[0].type='logarithmic';
casesLogChart.options.scales.yAxes[0].ticks.callback=logTicker;

var casesSlopeChart = new Chart($('#canvas-cases-slope')[0].getContext('2d'), derivativeConfig("Logarithmic Slope"))
var casesConChart = new Chart($('#canvas-cases-concavity')[0].getContext('2d'), derivativeConfig("Logarithmic Concavity"))


var deathsLinChart = new Chart($('#canvas-deaths-linear')[0].getContext('2d'), simpleConfig('Comfirmed Deaths'));
var deathsLogChart = new Chart($('#canvas-deaths-log')[0].getContext('2d'), simpleConfig('Comfirmed Deaths'));
deathsLogChart.options.scales.yAxes[0].type='logarithmic';
deathsLogChart.options.scales.yAxes[0].ticks.callback=logTicker;

var deathsSlopeChart = new Chart($('#canvas-deaths-slope')[0].getContext('2d'), derivativeConfig("Logarithmic Slope"))
var deathsConChart = new Chart($('#canvas-deaths-concavity')[0].getContext('2d'), derivativeConfig("Logarithmic Concavity"))

var recoveredLinChart = new Chart($('#canvas-recovered-linear')[0].getContext('2d'), simpleConfig('Comfirmed Recovered'));
var recoveredLogChart = new Chart($('#canvas-recovered-log')[0].getContext('2d'), simpleConfig('Comfirmed Recovered'));
recoveredLogChart.options.scales.yAxes[0].type='logarithmic';
recoveredLogChart.options.scales.yAxes[0].ticks.callback=logTicker;

var recoveredSlopeChart = new Chart($('#canvas-recovered-slope')[0].getContext('2d'), derivativeConfig("Logarithmic Slope"))
var recoveredConChart = new Chart($('#canvas-recovered-concavity')[0].getContext('2d'), derivativeConfig("Logarithmic Concavity"))

function submitSub(email,name,id){
  $.ajax({
          type: "POST",
          url: window.location.pathname+"subscribe",//other option is search
          dataType: "json",
          data : {email : email,
                  name : name,
                  countryCode:getCountryCode(id),
                  province:getProvince(id),
                  city:getCity(id)
                },
          success: function(response) {
              console.log(response);
          },
          error: function(response) {
              console.log(response);
          }
  });
   M.toast({html: 'All signed up!'})
}

function getCountryCode(id){
  return rawData["locations"][id]["country_code"]
}
function getProvince(id){
  pstr=rawData["locations"][id]["province"];
  if (pstr.split(",").length>1){
    console.log(pstr.split(",")[1])
    return statesDict[pstr.split(",")[1].trim()]
  }
  else if (pstr != ''){
    return pstr
  }
  return null
}
function getCity(id){
  pstr=rawData["locations"][id]["province"];
  if (pstr.split(",").length>1){
    statesDict[pstr.split(",")[1]]
    return pstr
  }
  return null
}
$.getJSON('https://coronavirus-tracker-api.herokuapp.com/v2/locations?timelines=0', function(response){
// $.getJSON('static/js/seeCOVID19/processed.json', function(response){
  rawData = response;
}).complete(function() {
  $.getJSON('static/js/seeCOVID19/supplyment.json', function(response){
  // $.getJSON('static/js/seeCOVID19/processed.json', function(response){
    console.log(response)
    rawData["locations"].push.apply(rawData["locations"],response)
  }).complete(function() {
  console.log("JSON loaded")
  console.log(rawData)
  $("#sub-signup").click(function(){submitSub($("#sub_email").val(),$("#sub_name").val(),currentID);
                                    M.Modal.getInstance(document.getElementById("subscribe-modal")).close();
                                    });
  $("#subscribe-open").click(function(){
    outStr=rawData["locations"][currentID]["country"]
    if(getProvince(currentID)!=null){
      outStr+=" "+getProvince(currentID)
    }
    if(getCity(currentID)!=null){
      outStr+=" "+getCity(currentID)
    }
    $("#subscribe-location").text(outStr);
  });
  updateCountryList()

  $('select').formSelect();

  $("#country-select").change(function () {
       var dataID = this.value;
       country=rawData["locations"][dataID]["country"]
       updateAllCharts(dataID)

       clearRegions()
       clearCities()
       updateRegionList(country)

   });
   $("#region-select").change(function () {
        var dataID = this.value;
        country=rawData["locations"][dataID]["country"]
        region=rawData["locations"][dataID]["province"]
        updateAllCharts(dataID)

        clearCities()
        updateCityList(country,region)
        M.toast({html: 'Some regions may not be fitted properly due to few data points or bad data'})

    });

    $("#municipality-select").change(function () {
         var dataID = this.value;
         country=rawData["locations"][dataID]["country"]
         city=rawData["locations"][dataID]["province"]
         region=statesDict[city.split(",")[1].trim()]
         console.log("updating",country,region,city)
         updateAllCharts(dataID)
         M.toast({html: 'Some municipalities may not be fitted properly due to few data points or bad data'})

     });

     function updateAllCharts(dataID){

       if (forgottenCountries.includes(rawData["locations"][dataID]["country"])){
         console.log("fixing forgotten country edge case, grabbing chart data")


        callList=[];
        for (locationID in rawData["locations"]){
          if (rawData["locations"][locationID]["country"]==rawData["locations"][dataID]["country"] &
              rawData["locations"][locationID]["province"]!='' ){
                APIurl='https://coronavirus-tracker-api.herokuapp.com/v2/locations/'+rawData["locations"][locationID]["id"]+'?source=jhu&timeline=1';
                callList.push($.getJSON(APIurl))
          }
        }

        Promise.all(callList).then(results => {
            // process results here
            console.log(results);      // from options1 request
            rawData["locations"][dataID] = combineRegions(results);
            repaintAllCharts(dataID)
        }).catch(err => {
            console.log(err);
        });


       }
       else{
         console.log("Normal, updating charts for ",dataID)
         APIurl='https://coronavirus-tracker-api.herokuapp.com/v2/locations/'+dataID+'?source=jhu';
         $.getJSON(APIurl, function(response){
           rawData["locations"][dataID] = response["location"];
         }).complete(function(){repaintAllCharts(dataID)})
       }

     }

     function repaintAllCharts(dataID) {

       $('#latest').text("Confirmed: "+rawData["locations"][dataID]["latest"]["confirmed"]+
                         "    Deaths: "   +rawData["locations"][dataID]["latest"]["deaths"]+
                         "    Recovered: "+rawData["locations"][dataID]["latest"]["recovered"]
                        );
        $("#data-ts").text("Data as of "+moment(rawData['locations'][dataID]["last_updated"]).format('MMMM Do YYYY, h:mm:ss a'))
       baselineData=getTimelineByID(dataID,type="confirmed")
       casesLinChart.data.datasets[1].data=baselineData
       casesLogChart.data.datasets[1].data=baselineData

       logConData=getLogConTimelineByID(dataID,type="confirmed")
       casesConChart.data.datasets[0].data=logConData

       logSlopeData=getLogSlopeTimelineByID(dataID,type="confirmed")
       casesSlopeChart.data.datasets[0].data=logSlopeData

       fittedData=getLogFitByID(dataID,type="confirmed")
       if (fittedData != {}){
         casesLinChart.data.datasets[0].data=fittedData
         casesLogChart.data.datasets[0].data=fittedData
       }

       casesLinChart.update()
       casesLogChart.update()
       casesConChart.update()
       casesSlopeChart.update()
        // -----------------------------------------------------------------------

       baselineData=getTimelineByID(dataID,type="deaths")
       deathsLinChart.data.datasets[1].data=baselineData
       deathsLogChart.data.datasets[1].data=baselineData

       logConData=getLogConTimelineByID(dataID,type="deaths")
       deathsConChart.data.datasets[0].data=logConData

       logSlopeData=getLogSlopeTimelineByID(dataID,type="deaths")
       deathsSlopeChart.data.datasets[0].data=logSlopeData

       fittedData=getLogFitByID(dataID,type="deaths")
       if (fittedData != {}){
         deathsLinChart.data.datasets[0].data=fittedData
         deathsLogChart.data.datasets[0].data=fittedData
       }

       deathsLinChart.update()
       deathsLogChart.update()
       deathsConChart.update()
       deathsSlopeChart.update()
       // ------------------------------------------------------------------------

       baselineData=getTimelineByID(dataID,type="recovered")
       recoveredLinChart.data.datasets[1].data=baselineData
       recoveredLogChart.data.datasets[1].data=baselineData

       logConData=getLogConTimelineByID(dataID,type="recovered")
       recoveredConChart.data.datasets[0].data=logConData

       logSlopeData=getLogSlopeTimelineByID(dataID,type="recovered")
       recoveredSlopeChart.data.datasets[0].data=logSlopeData

       fittedData=getLogFitByID(dataID,type="recovered")
       if (fittedData != {}){
         recoveredLinChart.data.datasets[0].data=fittedData
         recoveredLogChart.data.datasets[0].data=fittedData
       }

       recoveredLinChart.update()
       recoveredLogChart.update()
       recoveredConChart.update()
       recoveredSlopeChart.update()
       currentID=dataID
    }
    function combineRegions(regionsList){

    }
    function getForgottenList(){
      allLocations = new Set()
      uniqueCountries = new Set()
      for (var locationID in rawData["locations"]){
        allLocations.add(rawData["locations"][locationID]["country"])
        if (rawData["locations"][locationID]["province"]==''){
          uniqueCountries.add(rawData["locations"][locationID]["country"])
        }
      }
      return Array.from([...allLocations].filter(x => !uniqueCountries.has(x)))
    }
     function updateCountryList(){
       repaintCountryList();
       // forgottenCountries=getForgottenList()
       // for (i in forgottenCountries){
       //   console.log('FORGOTTEN! '+forgottenCountries[i])
       //   newObj={}
       //   newObj["country"]=forgottenCountries[i]
       //   newObj["country_code"]=isoCountries[forgottenCountries[i]]
       //   newObj["province"]="TBD"
       //   rawData["locations"].push(newObj)
       //
       //   APIurl='https://coronavirus-tracker-api.herokuapp.com/v2/locations?country_code='+isoCountries[forgottenCountries[i]]+'&source=jhu';
       //   $.getJSON(APIurl, function(response){
       //     console.log(response)
       //     newIDCtr=getIDbyLocation(response["locations"][0]["country"],'TBD')
       //     console.log("adding fotgotten coutnry back "+newIDCtr)
       //     console.log(response)
       //     rawData["locations"][newIDCtr]["latest"] = response["latest"]
       //     rawData["locations"][newIDCtr]["province"] = ""
       //   }).complete(function() {
       //     if(getForgottenList().length ==0){
       //       console.log("all fetched up!")
       //       repaintCountryList();
       //     }
       //   });
       // }

       // return countries
     }
     function repaintCountryList(){
       countriesArr =[]
       for (var locationID in rawData["locations"]){
         if (rawData["locations"][locationID]["province"]==''){
           console.log(rawData["locations"][locationID])
           countriesArr.push({country:rawData["locations"][locationID]["country"],id:locationID,cases:rawData["locations"][locationID]["latest"]["confirmed"]})
         }
       }
       // use Set to make sure there are no duplicates
       // countriesArr = Array.from(countries);
       countriesArr.sort(function(a, b) {return b.cases - a.cases;})
       // console.log(countriesArr)
       for (var i in countriesArr){
         console.log(countriesArr[i])
         if (i==0){
           addCountry(countriesArr[i],true)
           updateAllCharts(countriesArr[i]["id"])
         }
         else{
           addCountry(countriesArr[i],false)
         }
       }
     }
     function addCountry(countryObj,selected){
       // console.log("yeehaw "+countryObj["id"]+" "+countryObj["country"] )
       if (selected){
         $("#country-select").append('<option value="'+countryObj["id"]+'" selected>'+countryObj["country"]+'</option>')
       }
       else{
         $("#country-select").append('<option value="'+countryObj["id"]+'" >'+countryObj["country"]+'</option>')
       }
     }

     function updateRegionList(country){
       if (country== 'World'){
         console.log("world  detected")
         clearCities()
         clearRegions()
         $("#region-select").prop("disabled", true);
         $("#municipality-select").prop("disabled", true);
         $("#region-select").formSelect();
         $("#municipality-select").formSelect();
         return
       }
       if (isEmpty(mapDat[country])){
         console.log("disable region dropdown")
         $("#region-select").prop("disabled", true);
         $("#municipality-select").prop("disabled", true);
       }
       else{
         console.log("enable region dropdown")
         $("#region-select").prop("disabled", false);
         $("#municipality-select").prop("disabled", false);
         addRegion({province:"Overall",id:$('#country-select').val(),case:rawData["locations"][$('#country-select').val()]["latest"]["confirmed"]},true)
         var regionsList=[]
         for(region in mapDat[country]){
           for (var locationID in rawData["locations"]){
             // if (rawData["locations"][locationID]["country"]=="US"){
             //   console.log(rawData["locations"][locationID]["province"])
             // }
             if (rawData["locations"][locationID]["province"]==region){
               regionsList.push({province:region,id:locationID,cases:rawData["locations"][locationID]["latest"]["confirmed"]})
             }
           }
         }
         console.log(regionsList)
         regionsList.sort(function(a, b) {return b.cases - a.cases;})
         for (var i in regionsList){
           addRegion(regionsList[i],false)
         }
       }
       $("#region-select").formSelect();
       $("#municipality-select").formSelect();
     }
     function addRegion(regionObj,selected){
       console.log("Province: "+regionObj["id"]+" "+regionObj["province"] )
       if (selected){
         $("#region-select").append('<option value="'+regionObj["id"]+'" selected>'+regionObj["province"]+'</option>')
       }
       else{
         $("#region-select").append('<option value="'+regionObj["id"]+'" >'+regionObj["province"]+'</option>')
       }
     }
     function clearRegions(){
       $("#region-select").empty()
     }

     function updateCityList(country,region){

       if (region.trim() == ''){
         console.log("overall region detected")
         clearCities()
         $("#municipality-select").prop("disabled", true);
         $("#municipality-select").formSelect();
         return
       }
       if (isEmpty(mapDat[country][region])){
         console.log("disable city dropdown")
         $("#municipality-select").prop("disabled", true);
       }
       else{
         console.log("enable city dropdown")
         $("#municipality-select").prop("disabled", false);
         addCity({city:"Overall",id:$('#region-select').val(),case:rawData["locations"][$('#region-select').val()]["latest"]["confirmed"]},true)
         var citiesList=[]
         for(cityID in mapDat[country][region]){
           var city = mapDat[country][region][cityID]
           console.log(city)
           for (var locationID in rawData["locations"]){

             if (rawData["locations"][locationID]["province"]==city){
               citiesList.push({city:city,id:locationID,cases:rawData["locations"][locationID]["latest"]["confirmed"]})
             }
           }
         }
         console.log(citiesList)
         citiesList.sort(function(a, b) {return b.cases - a.cases;})
         for (var i in citiesList){
           addCity(citiesList[i],false)
         }
       }
       $("#municipality-select").formSelect();
     }
     function addCity(cityObj,selected){
       console.log("City: "+cityObj["id"]+" "+cityObj["city"] )
       if (selected){
         $("#municipality-select").append('<option value="'+cityObj["id"]+'" selected>'+cityObj["city"]+'</option>')
       }
       else{
         $("#municipality-select").append('<option value="'+cityObj["id"]+'" >'+cityObj["city"]+'</option>')
       }
     }
     function clearCities(){
       $("#municipality-select").empty()
     }


   });
});
function getIDbyLocation(country,province){
  for (locationID in rawData["locations"]){
    if (rawData["locations"][locationID]["country"] == country && rawData["locations"][locationID]["province"] == province){
      console.log("found ID!",locationID)
      return locationID
    }
  }
}
function getTimelineByID(locID,type="confirmed"){
  var data = [];
  var lastKey="";

  for(var key in rawData["locations"][locID]["timelines"][type]["timeline"]){
    var value = rawData["locations"][locID]["timelines"][type]["timeline"][key]
    // console.log(key,value)
    date= moment(key)
    if(rawData["locations"][locID]["timelines"][type]["timeline"][key] != rawData["locations"][locID]["timelines"][type]["timeline"][lastKey])
    data.push({
         t: date.valueOf(),
         y: value
       })
    lastKey=key
  }
 return data;
}
function getLogFitByID(locID,type="confirmed"){
  var data = [];
  var lastKey="";
  var outData=null;
  console.log(rawData["locations"][locID]["country"])
  $.ajax({
          type: "POST",
          url: window.location.pathname+"curveFit",//other option is search
          dataType: "json",
          async: false,
          data : JSON.stringify({series:getTimelineByID(locID,type)}),
          success: function(response) {
              // console.log(response);
              outData=response;
          },
          timeout: 3000,
          error: function(response) {
              console.log(response);
          }
  });
  if (outData==null){
    return null
  }
  console.log(outData);
  day0=moment(outData["day0"],'x')
  amplitude=outData["amplitude"]
  center=outData["center"]
  sigma=outData["sigma"]

 let future10  = moment(new Date()).add(10,'days');

 dt=0
 for (var m = day0; m.isBefore(future10); m.add(1, 'days')) {
   data.push({
        t: m.valueOf(),
        y: amplitude*(1-(1/(1+Math.exp((dt-center)/sigma))))
      })
   dt+=1;
 }

 return data;
}
function getLogConTimelineByID(locID,type="confirmed"){
 var inData= getLogSlopeTimelineByID(locID,"confirmed")
 iterCnt=0;
 lastVal=0;
 var outData=[];
 for (var key in inData){
   val=inData[key]["y"]
   if(iterCnt>=1){
     outData.push({
          t: inData[key]["t"],
          y: val-lastVal
        })
   }
   lastVal=val
   iterCnt+=1;
 }
 return outData;
}

function getLogSlopeTimelineByID(locID,type="confirmed"){

 var inData= getTimelineByID(locID,"confirmed")
 // console.log(inData)
 iterCnt=0;
 lastVal=0;
 var outData=[];
 for (var key in inData){
   val=Math.log10(inData[key]["y"])
   if(iterCnt>=1){
     outData.push({
          t: inData[key]["t"],
          y: val-lastVal
        })
   }
   lastVal=val
   iterCnt+=1;
 }
 return outData;
}


function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

$(document).ready(function(){
  M.AutoInit();
    // $('.tabs').tabs();
    // $('.collapsible').collapsible();
    // $('.modal').modal();

});
