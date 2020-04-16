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

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

var isoCountries = {
        'Cruise Ship': 'XX',
        'Australia': 'AU',
        'Canada': 'CA',
        'China': 'CN',
        'United States': 'US',
    };

var rawData={}
var currentID=0;
var getKey = (mapData,val) => Object.keys(mapData).find(key => mapData[key]["id"] == val);
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
                  },
                  unit: 'day'
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
                  },
                  unit: 'day'
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

var activeLinChart = new Chart($('#canvas-active-linear')[0].getContext('2d'), simpleConfig('Comfirmed active'));
var activeLogChart = new Chart($('#canvas-active-log')[0].getContext('2d'), simpleConfig('Comfirmed active'));
activeLogChart.options.scales.yAxes[0].type='logarithmic';
activeLogChart.options.scales.yAxes[0].ticks.callback=logTicker;

var activeSlopeChart = new Chart($('#canvas-active-slope')[0].getContext('2d'), derivativeConfig("Logarithmic Slope"))
var activeConChart = new Chart($('#canvas-active-concavity')[0].getContext('2d'), derivativeConfig("Logarithmic Concavity"))

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
  return rawData[id]["country_code"]
}
function getProvince(id){
  pstr=rawData[id]["province"];
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
  pstr=rawData[id]["province"];
  if (pstr.split(",").length>1){
    statesDict[pstr.split(",")[1]]
    return pstr
  }
  return null
}
$.getJSON('COVID19map', function(response){
// $.getJSON('static/js/seeCOVID19/processed.json', function(response){
  mapData = response;
  // $.getJSON('static/js/seeCOVID19/processed.json', function(response){
  console.log(response)
  }).complete(function() {
  console.log("JSON loaded")
  $("#sub-signup").click(function(){submitSub($("#sub_email").val(),$("#sub_name").val(),currentID);
                                    M.Modal.getInstance(document.getElementById("subscribe-modal")).close();
                                    });
  $("#subscribe-open").click(function(){
    outStr=rawData[currentID]["country"]
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
       country=getKey(mapData,dataID)
       console.log("Found key",country,dataID)
       updateAllCharts(dataID)

       clearRegions()
       clearCities()
       updateRegionList(country)

   });
   $("#region-select").change(function () {
        var dataID = this.value;
        console.log(dataID)
        country=getKey(mapData,$('#country-select').val())
        region=getKey(mapData[country]["provinces"],dataID)

        updateAllCharts(dataID)

        clearCities()
        updateCityList(country,region)
        M.toast({html: 'Some regions may not be fitted properly due to few data points or bad data'})

    });

    $("#municipality-select").change(function () {
         var dataID = this.value;
         // country=getKey(mapData,$('#country-select').val())
         // region=getKey(mapData[country]["provinces"],$('#region-select'))
         // city=getKey(mapData[country]["provinces"][region]["cities"],dataID)
         // console.log("updating",country,region,city)
         updateAllCharts(dataID)
         M.toast({html: 'Some municipalities may not be fitted properly due to few data points or bad data'})

     });

     function updateAllCharts(dataID){

       console.log("Normal, updating charts for ",dataID)
       APIurl='COVID19timeseries?id='+dataID;
       $.getJSON(APIurl, function(response){
         rawData[dataID] = response;
         console.log(rawData)
       }).complete(function(){
         targetType=2
         city=$("#municipality-select option:selected").text()
         state=$("#region-select option:selected").text()
         if (city=="Overall" | city == ''){
           city=""
           targetType=1
         }
         if (state=="Overall" | state == ''){
           state=""
           targetType=0
         }

         country=$("#country-select option:selected").text()
         console.log("Updating dem data",targetType,country,state,city)
         $.ajax({
                 type: "GET",
                 url: window.location.pathname+"dem",//other option is search
                 dataType: "json",
                 data : {country:country,state:state,county:city},
                 success: function(response) {
                     // console.log(response);

                     outData=response;
                     pop=outData["pop"]
                     density=outData["density"]
                     rawData[dataID]["pop"]=pop
                     rawData[dataID]["density"]=density
                     unit="square kilometer"
                     if(targetType==0){
                       comfirmed=mapData[country]["cases"]
                       outStr=country
                       if(country=="US"){unit="square mile"}
                     }
                     else if(targetType==1){
                       comfirmed=mapData[country]["provinces"][state]["cases"]
                       outStr=state+", "+country
                       unit="square mile"
                     }
                     else if(targetType==2){
                       comfirmed=mapData[country]["provinces"][state]["cities"][city]["cases"]
                       outStr=city+", "+state+", "+country
                       unit="square mile"
                     }

                     odds=Math.round(pop/comfirmed)
                     console.log("odds here",odds,pop,comfirmed)
                     ratio=density/odds
                     if (ratio>1){
                       ratio1=Math.round(ratio)
                       densityRatioStr=ratio1+" cases per "+unit
                     }
                     else{
                       ratio2=Math.round(1/ratio)
                       densityRatioStr="1 cases every "+ratio2+" "+unit+"s"
                     }

                     $("#subscribe-location").text(outStr);
                     $("#demo-statement").html("@ "+outStr+"<br> 1 in "+odds+" people have Coronavirus<br>That's "+densityRatioStr)

                     $(".chance-covid").remove()
                     cardHtml='<li class="collection-item chance-covid"> <div class="valign-wrapper"><img src="/static/img/seeCOVID19/virus.png"><p>1 in&nbsp;<b class="odds">'+odds+'</b>&nbsp;chance: you have COVID-19 @ '+outStr+'</p></div></li>'
                     $('#odds li .odds').each(function(i, obj) {
                        itemOdd=parseInt($(obj).text());
                        if(odds<itemOdd){
                          $(obj).parent().parent().parent().before(cardHtml);
                          return false
                        }
                     });
                     $("#demographics").show()
                 },
                 timeout: 3000,
                 error: function(response) {
                     console.log(response);
                     console.log("no dem data found")
                     $("#demographics").hide()
                 },
                 complete: function(){
                   repaintAllCharts(dataID)
                 }
         });
       });




     }

     function repaintAllCharts(dataID) {

       statusText="Confirmed: "+numberWithCommas(rawData[dataID]["latest"]["confirmed"])+
                         "    Deaths: "   +numberWithCommas(rawData[dataID]["latest"]["deaths"])
       if(rawData[dataID]["latest"]["recovered"]!=0){
         statusText+="    Recovered: "+numberWithCommas(rawData[dataID]["latest"]["recovered"])
         $(".recovered-div").show()
         $(".active-div").show()
      }
      else{
        $(".recovered-div").hide()
        $(".active-div").hide()

      }
       $('#latest').text(statusText);
        $("#data-ts").text("Data as of "+moment(rawData[dataID]["last_updated"]).add(7,"hours").format('MMMM Do YYYY'))
       baselineData=getTimelineByID(dataID,type="confirmed")
       casesLinChart.data.datasets[1].data=baselineData
       casesLogChart.data.datasets[1].data=baselineData

       logConData=getLogConTimelineByID(dataID,type="confirmed")
       casesConChart.data.datasets[0].data=logConData

       logSlopeData=getLogSlopeTimelineByID(dataID,type="confirmed")
       casesSlopeChart.data.datasets[0].data=logSlopeData

       getLogFitByID(dataID,type="confirmed")

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

       getLogFitByID(dataID,type="deaths")

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

       getLogFitByID(dataID,type="recovered")

       recoveredLinChart.update()
       recoveredLogChart.update()
       recoveredConChart.update()
       recoveredSlopeChart.update()
       // ------------------------------------------------------------------------

       baselineData=getTimelineByID(dataID,type="active")
       activeLinChart.data.datasets[1].data=baselineData
       activeLogChart.data.datasets[1].data=baselineData

       logConData=getLogConTimelineByID(dataID,type="active")
       activeConChart.data.datasets[0].data=logConData

       logSlopeData=getLogSlopeTimelineByID(dataID,type="active")
       activeSlopeChart.data.datasets[0].data=logSlopeData

       getSIRFitByID(dataID)

       activeLinChart.update()
       activeLogChart.update()
       activeConChart.update()
       activeSlopeChart.update()
       // ------------------------------------------------------------------------

       currentID=dataID
    }

     function updateCountryList(){
       repaintCountryList();
     }
     function repaintCountryList(){
       countriesArr =[]
       for (var country in mapData){
           console.log(mapData[country]["id"],mapData[country]["cases"])
           countriesArr.push({country:country,id:mapData[country]["id"],cases:mapData[country]["cases"]})

       }

       countriesArr.sort(function(a, b) {return b.cases - a.cases;})

       for (var i in countriesArr){
         // console.log(countriesArr[i])
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
       if (isEmpty(mapData[country]["provinces"])){
         console.log("disable region dropdown")
         $("#region-select").prop("disabled", true);
         $("#municipality-select").prop("disabled", true);
       }
       else{
         console.log("enable region dropdown")
         $("#region-select").prop("disabled", false);
         $("#municipality-select").prop("disabled", false);
         addRegion({province:"Overall",id:$('#country-select').val(),cases:mapData[country]["cases"]},true)
         var regionsList=[]
         for(province in mapData[country]["provinces"]){
           console.log(province)
           regionsList.push({province:province,id:mapData[country]["provinces"][province]["id"],cases:mapData[country]["provinces"][province]["cases"]})
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
       // console.log(country,region)
       if (region == undefined){
         console.log("overall city detected")
         clearCities()
         $("#municipality-select").prop("disabled", true);
         $("#municipality-select").formSelect();
         return
       }
       else if (isEmpty(mapData[country]["provinces"][region]["cities"])){
         console.log("disable city dropdown")
         $("#municipality-select").prop("disabled", true);
       }
       else{
         console.log("enable city dropdown")
         $("#municipality-select").prop("disabled", false);
         addCity({city:"Overall",id:$('#region-select').val(),case:mapData[country]["provinces"][region]["cases"]},true)

         var citiesList=[]
         for(city in mapData[country]["provinces"][region]["cities"]){
            console.log(city)
            citiesList.push({city:city,id:mapData[country]["provinces"][region]["cities"][city]["id"],cases:mapData[country]["provinces"][region]["cities"][city]["cases"]})
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
function getIDbyLocation(country,province){
  for (locationID in rawData){
    if (rawData[locationID]["country"] == country && rawData[locationID]["province"] == province){
      console.log("found ID!",locationID)
      return locationID
    }
  }
}
function getTimelineByID(locID,type="confirmed"){
  var data = [];
  var lastKey="";
  if (type=="active" & rawData[locID]["latest"]["comfirmed"]!=0){
    console.log("calculating activ cases")
    for(var key in rawData[locID]["confirmed"]){
      // console.log(key)
      var convalue = rawData[locID]["confirmed"][key]
      var recvalue = rawData[locID]["recovered"][key]
      var value=convalue-recvalue
      // console.log(convalue,recvalue)
      // console.log(key,value)
      date= moment(key).add(7, 'hours')
      // if(rawData[locID]["comfirmed"][key] != rawData[locID]["comfirmed"][lastKey])
      data.push({
           t: date.valueOf(),
           y: value
         })
      lastKey=key

    }
  }
  else{
    for(var key in rawData[locID][type]){
      var value = rawData[locID][type][key]
      // console.log(key,value)
      date= moment(key).add(7, 'hours')
      if(rawData[locID][type][key] != rawData[locID][type][lastKey])
      data.push({
           t: date.valueOf(),
           y: value
         })
      lastKey=key

    }
  }
  data.sort(function(a, b) {return a.t - b.t;})
 return data;
}
function updateLogFitByID(outData,type){
  console.log("in update log callback!")
  if (outData==null){
    return null
  }
  console.log(outData);
  day0=moment(outData["day0"],'x')
  amplitude=outData["amplitude"]
  center=outData["center"]
  sigma=outData["sigma"]

 let future10  = moment(new Date()).add(10,'days');
 data=[]
 dt=0
 for (var m = day0; m.isBefore(future10); m.add(1, 'days')) {
   data.push({
        t: m.valueOf(),
        y: amplitude*(1-(1/(1+Math.exp((dt-center)/sigma))))
      })
   dt+=1;
 }

  if (data != {}){
    if(type=="confirmed"){
      casesLinChart.data.datasets[0].data=data
      casesLogChart.data.datasets[0].data=data
      casesLinChart.update()
      casesLogChart.update()
    }
    else if(type=="deaths"){
      deathsLinChart.data.datasets[0].data=data
      deathsLogChart.data.datasets[0].data=data
      deathsLinChart.update()
      deathsLogChart.update()
    }
    else if(type=="recovered"){
      recoveredLinChart.data.datasets[0].data=data
      recoveredLogChart.data.datasets[0].data=data
      recoveredLinChart.update()
      recoveredLogChart.update()
    }
  }
}

function getLogFitByID(locID,type="confirmed"){
  var data = [];
  var lastKey="";
  var outData=null;
  console.log(rawData[locID]["country"])
  $.ajax({
          type: "POST",
          url: window.location.pathname+"curveFit",//other option is search
          dataType: "json",
          data : JSON.stringify({series:getTimelineByID(locID,type)}),
          success: function(response) {
              // console.log(response);
              outData=response;
              updateLogFitByID(outData,type)
          },
          timeout: 3000,
          error: function(response) {
              console.log(response);
          }
  });

}

function getSIRFitByID(locID){
  var data = [];
  var lastKey="";
  var outData=null;
  console.log("kicking off SIR fit",locID)
  ohHere=rawData[locID]
  pop=ohHere.pop
  console.log(ohHere)
  console.log(pop)
  console.log({series:getTimelineByID(locID,"active"),pop:rawData[locID]["pop"]})
  $.ajax({
          type: "POST",
          url: window.location.pathname+"SIRFit",//other option is search
          dataType: "json",
          data : JSON.stringify({series:getTimelineByID(locID,"active"),pop:rawData[locID]["pop"]}),
          success: function(response) {
              // console.log(response);
              outData=response;
              console.log(outData)
              // updateLogFitByID(outData,type)
          },
          timeout: 3000,
          error: function(response) {
              console.log(response);
          }
  });

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
