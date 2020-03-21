
// var topWords= {"trump":null,"goverment shutdown":null,"muller investigation":null,"travewar":null,"border":null,"immigration":null,"abortion":null,"supreme court":null,"police":null,"south china sea":null,"democrats":null,"republicans":null,"syria":null,"mexico":null,"senate":null,"white house":null,"california":null,"election":null,"africa":null,"education":null,"nancy pelosi":null,"campaign":null};

// $('#search').autocomplete({
//     data:topWords,
//     onAutocomplete: function(val){
//           console.log(val);
//           if($("#topic-"+val.replace(/\s+/g, '-').toLowerCase()).length){
//             $([document.documentElement, document.body]).animate({
//                   scrollTop: $("#topic-"+val.replace(/\s+/g, '-').toLowerCase()).offset().top-100
//               }, 1000);
//           }
//           else{
//             insertNewCard(val);
//           }
//       }
//   });

activeTopic=''
document.getElementById('search').onkeypress = function(e){
    if (!e) e = window.event;
    var keyCode = e.keyCode || e.which;
    if (keyCode == '13'){
      // Enter pressed
      // console.log("dude")
      // console.log($("#search").val())
        activeTopic=$("#search").val();
        console.log("searched for "+activeTopic)
        $(".pre-spin-loader").show()
        $(".card-rack").html(" "); // clear html
        idsList=[]; // clear id list
        appendNewCard(10,endpoint="search");
        loading=false;
      return false;
    }
  }

var idsList=[]
var stuck=false;
var loadSense=200;
var loading=true;
$(".small-title").hide();
$(".small-title").css("opacity",0);
$(".spin-loader").css("opacity",0)

$(document).ready(function(){
    $('.tabs').tabs(); // { swipeable: true }
    $('select').formSelect();
  });

function appendNewCard(length,endpoint="load"){
    console.log("trying to append new card")
    var site = $("#site-select input").val()
          $.ajax({
                  type: "POST",
                  url: window.location.pathname+endpoint,//other option is search
                  dataType: "json",
                  data : {ids : idsList,site:site,query:activeTopic,length:length},
                  success: function(response) {
                      console.log(response);
                      $(".card-rack").append(response.card);
                      $(".pre-spin-loader").hide()
                      idsList=idsList.concat(response.ids);
                      // console.log("adding qid "+response.context.question.id);
                      // idsList.push(response.context.question.id);
                      loading=false;
                      $(".spin-loader").css("opacity",0)
                  },
                  error: function(response) {
                      console.log(response);
                  }
          });
};

$(window).scroll(animate_scroll);
function animate_scroll(){
  if ($(window).scrollTop()-$('.card-rack').offset().top+120 >0 & !stuck){
    stuck=true;
    console.log("stuck");
    $('nav').addClass('s8').removeClass('s12');
    setTimeout(function() {
      console.log("calling left toggle");
      $(".small-title").show();

    }, 500);
    setTimeout(function() {
      console.log("calling left toggle 2");
      $(".small-title").css("opacity",1);
    }, 600);
  }

  else if ($(window).scrollTop()-$('.card-rack').offset().top+120 <0 & stuck){
    stuck=false;
    console.log("un stuck");
    $(".small-title").css("opacity",0);
    setTimeout(function() {
      console.log("calling right toggle");
      $(".small-title").hide();
      $('nav').addClass('s12').removeClass('s8');
    }, 500);
  }
  // else if ($(window).scrollTop()-($('.card-rack').offset().top+$('.card-rack').height())+$(window).height()+loadSense > 0 & !loading){
  //   loading=true;
  //   $(".spin-loader").css("opacity",1)
  //   console.log("starting to load");
  //   appendNewCard(1);
  // }

}
