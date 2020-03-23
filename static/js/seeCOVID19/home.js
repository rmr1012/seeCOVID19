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


var rawData

var ctx = document.getElementById('canvas-cases-linear').getContext('2d');
var casesLinChart = new Chart(ctx, {
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
            labelString: 'Comfirmed Cases'
          }
        }]
      },
    }
});

var ctx = document.getElementById('canvas-cases-log').getContext('2d');
var casesLogChart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        datasets: [{
          label: 'Fitted Logistic Curve',
          fill:false,
          borderDash:[5,5],
          backgroundColor: 'rgb(50, 50, 230)',
          borderColor: 'rgb(50, 50, 230)',
          order:2,
        },{
            label: 'Recorded Data',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            order: 1
        }  ]
    },

    // Configuration options go here
    options: {
      responsive: true,
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
            labelString: 'Comfirmed Cases'
          },
          type: 'logarithmic',
          ticks:{
            callback: function(...args) {
               const value = Chart.Ticks.formatters.logarithmic.call(this, ...args);
               // console.log(value)
               if (value.length) {
                 return Number(value).toLocaleString()
               }
               return value;
             }
          }
        }]
      }
    }
});


var ctx = document.getElementById('canvas-cases-slope').getContext('2d');
var casesSlopeChart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        datasets: [
          {
            label: 'Logarithmic Slope',
            fill:false,
            backgroundColor: 'rgb(50, 50, 230)',
            borderColor: 'rgb(50, 50, 230)',
          }]
    },

    // Configuration options go here
    options: {
      responsive: true,
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
            labelString: 'Comfirmed Cases'
          }
        }]
      },
    }


});

var ctx = document.getElementById('canvas-cases-concavity').getContext('2d');
var casesConChart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        datasets: [
          {
            label: 'Logarithmic Concavity',
            fill:false,
            backgroundColor: 'rgb(50, 50, 230)',
            borderColor: 'rgb(50, 50, 230)',
          }]
    },

    // Configuration options go here
    options: {
      responsive: true,
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
            labelString: 'Comfirmed Cases'
          }
        }]
      },
    }


});


$.getJSON('static/js/seeCOVID19/processed.json', function(response){
  rawData = response;
}).complete(function() {
  console.log("JSON loaded")
  console.log(rawData)


  updateCountryList(rawData)

  $('select').formSelect();

  $("#country-select").change(function () {
       var dataID = this.value;
       country=rawData["locations"][dataID]["country"]
       updateAllCharts(dataID)

       clearRegions()
       clearCities()
       updateRegionList(rawData,country)

   });
   $("#region-select").change(function () {
        var dataID = this.value;
        country=rawData["locations"][dataID]["country"]
        region=rawData["locations"][dataID]["province"]
        updateAllCharts(dataID)

        clearCities()
        updateCityList(rawData,country,region)

    });

    $("#municipality-select").change(function () {
         var dataID = this.value;
         country=rawData["locations"][dataID]["country"]
         city=rawData["locations"][dataID]["province"]
         region=statesDict[city.split(",")[1].trim()]
         console.log("updating",country,region,city)
         updateAllCharts(dataID)

     });

     function updateAllCharts(dataID){
       $('#latest').text("Confirmed: "+rawData["locations"][dataID]["latest"]["confirmed"]+
                         " Deaths: "   +rawData["locations"][dataID]["latest"]["deaths"]+
                         " Recovered: "+rawData["locations"][dataID]["latest"]["recovered"]
                        );
       baselineData=getTimelineByID(dataID,type="confirmed")
       casesLinChart.data.datasets[1].data=baselineData
       casesLinChart.options.title.text="Data as of "+moment(rawData['locations'][dataID]["last_updated"]).format('MMMM Do YYYY, h:mm:ss a')

       casesLogChart.data.datasets[1].data=baselineData
       casesLogChart.options.title.text="Data as of "+moment(rawData['locations'][dataID]["last_updated"]).format('MMMM Do YYYY, h:mm:ss a')

       logConData=getLogConTimelineByID(dataID,type="confirmed")
       casesConChart.data.datasets[0].data=logConData
       casesConChart.options.title.text="Data as of "+moment(rawData['locations'][dataID]["last_updated"]).format('MMMM Do YYYY, h:mm:ss a')

       logSlopeData=getLogSlopeTimelineByID(dataID,type="confirmed")
       casesSlopeChart.data.datasets[0].data=logSlopeData
       casesSlopeChart.options.title.text="Data as of "+moment(rawData['locations'][dataID]["last_updated"]).format('MMMM Do YYYY, h:mm:ss a')


       if (rawData["locations"][dataID]["timelines"][type]["logistic_fit"]["fitted"]){
         fittedData=getLogFitByID(dataID,type="confirmed")
         casesLinChart.data.datasets[0].data=fittedData
         casesLogChart.data.datasets[0].data=fittedData
       }

       casesLinChart.update()
       casesLogChart.update()
       casesConChart.update()
       casesSlopeChart.update()
     }
     function updateCountryList(data){
       countries = new Set()
       for (var locationID in rawData["locations"]){
         // if (rawData["locations"][locationID]["country"]=="US"){
         //   console.log(rawData["locations"][locationID]["province"])
         // }
         if (rawData["locations"][locationID]["province"]==''){
           countries.add({country:rawData["locations"][locationID]["country"],id:locationID,cases:rawData["locations"][locationID]["latest"]["confirmed"]})
         }
       }
       // use Set to make sure there are no duplicates
       countriesArr = Array.from(countries);
       countriesArr.sort(function(a, b) {return b.cases - a.cases;})
       // console.log(countriesArr)
       for (var i in countriesArr){
         // console.log(countriesArr[locationID])
         if (i==0){
           addCountry(countriesArr[i],true)
           updateAllCharts(countriesArr[i]["id"])
         }
         else{
           addCountry(countriesArr[i],false)
         }
       }
       // return countries
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

     function updateRegionList(data,country){
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
       if (isEmpty(data["map"][country])){
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
         for(region in data["map"][country]){
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

     function updateCityList(data,country,region){

       if (region.trim() == ''){
         console.log("overall region detected")
         clearCities()
         $("#municipality-select").prop("disabled", true);
         $("#municipality-select").formSelect();
         return
       }
       if (isEmpty(data["map"][country][region])){
         console.log("disable city dropdown")
         $("#municipality-select").prop("disabled", true);
       }
       else{
         console.log("enable city dropdown")
         $("#municipality-select").prop("disabled", false);
         addCity({city:"Overall",id:$('#region-select').val(),case:rawData["locations"][$('#region-select').val()]["latest"]["confirmed"]},true)
         var citiesList=[]
         for(cityID in data["map"][country][region]){
           var city = data["map"][country][region][cityID]
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

     function getIDTopDown(data,country,region,city){

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

       day0=moment(rawData["locations"][locID]["timelines"][type]["logistic_fit"]["values"]["day0"])
       amplitude=rawData["locations"][locID]["timelines"][type]["logistic_fit"]["values"]["amplitude"]
       center=rawData["locations"][locID]["timelines"][type]["logistic_fit"]["values"]["center"]
       sigma=rawData["locations"][locID]["timelines"][type]["logistic_fit"]["values"]["sigma"]

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
      var data = [];
      var lastKey="";
      for(var key in rawData["locations"][locID]["timelines"][type]["log_concavity_timeline"]){
        var value = rawData["locations"][locID]["timelines"][type]["log_concavity_timeline"][key]
        console.log(key,value)
        date= moment(key)
        if(rawData["locations"][locID]["timelines"][type]["log_concavity_timeline"][key] != rawData["locations"][locID]["timelines"][type]["log_concavity_timeline"][lastKey])
        data.push({
             t: date.valueOf(),
             y: value
           })
        lastKey=key
      }
     return data;
    }

    function getLogSlopeTimelineByID(locID,type="confirmed"){
      var data = [];
      var lastKey="";
      for(var key in rawData["locations"][locID]["timelines"][type]["log_slope_timeline"]){
        var value = rawData["locations"][locID]["timelines"][type]["log_slope_timeline"][key]
        console.log(key,value)
        date= moment(key)
        if(rawData["locations"][locID]["timelines"][type]["log_slope_timeline"][key] != rawData["locations"][locID]["timelines"][type]["log_slope_timeline"][lastKey])
        data.push({
             t: date.valueOf(),
             y: value
           })
        lastKey=key
      }
     return data;
    }

});




function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

$(document).ready(function(){

    $('.tabs').tabs();

});
