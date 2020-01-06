$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});

$( ".menu-btn" ).click(function() {
  $( 'body' ).toggleClass( "sidebar-active" );
});

$( ".open-search" ).click(function() {
  $('.search-option').addClass( "d-block" );
});
$( ".close-search, .share-popup-backdrop" ).click(function() {
  $('.search-option').removeClass( "d-block" );
});

$('.video-slider').slick({ 
   slidesToShow: 6,
   slidesToScroll: 6,
   arrows: true,
   dots: false,
   loop: false,   
   autoplay: false,
   autoplaySpeed:4000,
   prevArrow:"<button type='button' class='slick-prev'><i class='fas fa-chevron-left'></i></button>",
   nextArrow:"<button type='button' class='slick-next'><i class='fas fa-chevron-right'></i></button>",
   responsive: [
     {
       breakpoint: 1920,
       settings: {
         slidesToShow: 5,
         slidesToScroll: 5,
       }
     }, 
     {
       breakpoint: 1600,
       settings: {
         slidesToShow: 4,
         slidesToScroll: 4,
       }
      },
      {
         breakpoint: 1367,
         settings: {
            slidesToShow: 3,
            slidesToScroll: 3,
         }
      }, 
     {
       breakpoint: 992,
       settings: {
         slidesToShow: 2,
         slidesToScroll: 2,
       }
     },
     {
      breakpoint: 769,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
      }
    }, 
   ]
 });

 $('.recomendado-slider').slick({ 
   slidesToShow: 3,
   slidesToScroll: 3,
   arrows: true,
   dots: false,
   loop: false,   
   autoplay: false,
   autoplaySpeed:4000,
   prevArrow:"<button type='button' class='slick-prev'><i class='fas fa-chevron-left'></i></button>",
   nextArrow:"<button type='button' class='slick-next'><i class='fas fa-chevron-right'></i></button>",
   responsive: [
     {
       breakpoint: 1367,
       settings: {
         slidesToShow: 2,
         slidesToScroll: 2,
       }
     }, 
     {
       breakpoint: 769,
       settings: {
         slidesToShow: 1,
         slidesToScroll: 1,
       }
     }, 
   ]
 });

$( ".like-action button" ).click(function() {
  $('.like-action button').removeClass( "active" ); 
  $(this).toggleClass( "active" );
});
$( ".video-share" ).click(function() {
  $('.share-popup').addClass( "active" );
});
$( ".close-share, .share-popup-backdrop" ).click(function() {
  $('.share-popup').removeClass( "active" );
});



$( ".reply-more-btn" ).click(function() {
  $(this).toggleClass( "active" ); 
});

$( ".readmore" ).click(function() {
  $(this).toggleClass( "active" );
  $('#video-full-desp').toggleClass( "active" ); 
});

try{
  var textarea = document.querySelector('.comment-field');
  textarea.addEventListener('keydown', autosize);
  function autosize(){
    var el = this;
    setTimeout(function(){
      el.style.cssText = 'height:auto';
      el.style.cssText = 'height:' + el.scrollHeight + 'px';
    },0);
  }
} catch(ed){
  console.log(ed)
}