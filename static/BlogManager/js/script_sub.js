$('.effect').on('inview', function() {
	 var $item = $(this);
	 $item.addClass('start');
});

var $header = $('header');

var w_h = $(window).height();
var topBtn = $('.to_top');


if ((navigator.userAgent.indexOf('iPhone') > 0 && navigator.userAgent.indexOf('iPad') == -1) || navigator.userAgent.indexOf('iPod') > 0 || navigator.userAgent.indexOf('Android') > 0) {


$(window).scroll(function () {

        if ($(this).scrollTop() > 100 && menuOpen == false) {
            topBtn.fadeIn();
        } else {
            topBtn.fadeOut();
        }
    });
} else {


$(window).scroll(function () {
	var w_h = $(window).height();
		var s_top = $(this).scrollTop(); //スクロールの値を取得
		var l_top = w_h / 2;
		var ml_top = l_top + s_top / 2;

        if ($(this).scrollTop() > 100 && menuOpen == false) {
            topBtn.fadeIn();
        } else {
            topBtn.fadeOut();
        }
		 if ($(window).scrollTop() > 300) {
                $header.addClass('fixed');
            } else {
                $header.removeClass('fixed');
            }
    });
}

$(function(){
	
	topBtn.hide();

$('a[href^=#]').click(function(){
var speed = 500;
var href= $(this).attr("href");
var target = $(href == "#" || href == "" ? 'html' : href);
var position = target.offset().top;
$("html, body").animate({scrollTop:position}, speed, "swing");
return false;
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

// サイトアクセス時フェードイン 
$(function(){
 
    $('body').hide();
    $('body').fadeIn(300);
     
});

$(window).fadeThis();
