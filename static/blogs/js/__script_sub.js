$('.effect').on('inview', function() {
	 var $item = $(this);
	 $item.addClass('start');
});

$(function(){
$('a[href^=#]').click(function(){
var speed = 500;
var href= $(this).attr("href");
var target = $(href == "#" || href == "" ? 'html' : href);
var position = target.offset().top;
$("html, body").animate({scrollTop:position}, speed, "swing");
return false;
});
});

//トップへ戻るボタン
$(function() {
    var topBtn = $('.to_top');   
    topBtn.hide();
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            topBtn.fadeIn();
        } else {
            topBtn.fadeOut();
        }
    });
});


$(function(){
    $(window).bind("scroll", function() {
    scrollHeight = $(document).height();
    scrollPosition = $(window).height() + $(window).scrollTop();
    footHeight = $("footer").height();

    if ( scrollHeight - scrollPosition  <= footHeight ) {
        $(".to_top").css({"position":"fixed","bottom": footHeight});
    } else {
        $(".to_top").css({"position":"fixed","bottom": "10px"});
        }
    });
});

//スマホメニュー
var bnrBtn = $('#g_navi');
var bnrBtn2 = $('#h_box_sp');
var menuOpen = false;
var scrollpos;

$('.bg_bl').hide();

var ttt = false;

$(function(){
        $(".menu_btn").on("click", function() {
	if(ttt == false) {
          bnrBtn.stop().animate({'left' : '20%'}, 300);
		  bnrBtn2.stop().animate({'left' : '0%'}, 300);
          menuOpen = true;
		  $('.om').hide();
		  $('.to_top').hide();
		  $('.bg_bl').fadeIn();
		  scrollpos = $(window).scrollTop();
      $('body').addClass('fixed').css({'top': -scrollpos});
	        $(".menu_btn").addClass('opened');
	  ttt = true;
	} else {
		bnrBtn.stop().animate({'left' : '100%'}, 300);
		  bnrBtn2.stop().animate({'left' : '100%'}, 300);
          menuOpen = false;
		  $('.om').show();
		  $('.bg_bl').fadeOut();
		  $('body').removeClass('fixed').css({'top': 0});
		  $(".menu_btn").removeClass('opened');
      window.scrollTo( 0 , scrollpos );
	  ttt = false;
	}
        });
});

	 
$(window).resize(function(){
    var w = $(window).width();
    var x = 960;
    if (w >= x) {
		bnrBtn.stop().animate({'left' : '100%'}, 300);
		bnrBtn2.stop().animate({'left' : '100%'}, 300);
        menuOpen = false;
		$('.bg_bl').hide();
		ttt = false;
		$(".menu_btn").removeClass('opened');
    }
});

//アコーディオン
$(function(){
        $(".ac_menu").on("click", function() {
            $(this).next().slideToggle(); 
            $(this).toggleClass("active"); 
        });
});


var $header = $('header');
$(window).scroll(function () {
		 if ($(window).scrollTop() > 300) {
                $header.addClass('fixed');
            } else {
                $header.removeClass('fixed');
            }
});


// サイトアクセス時フェードイン 
$(function(){
 
    $('body').hide();
    $('body').fadeIn(300);
     
});

$(window).fadeThis();