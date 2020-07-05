$(document).ready(function(){


  $(".submenu > a").click(function(e) {
    e.preventDefault();
    var $li = $(this).parent("li");
    var $ul = $(this).next("ul");

    if($li.hasClass("open")) {
      $ul.slideUp(350);
      $li.removeClass("open");
    } else {
      $(".nav > li > ul").slideUp(350);
      $(".nav > li").removeClass("open");
      $ul.slideDown(350);
      $li.addClass("open");
    }
  });
  
});

function submitCheck(submit_type){
  switch (submit_type) {
    case "create":
      var title = $('#id_title').val();
      var str = "タイトル「" + title +"」を投稿してよろしいですか？";
      break;

    case "delete":
      var obj = event.target;
      var title = obj.closest('tr').children[0].textContent.trim();
      var str = "タイトル「" + title +"」を削除してよろしいですか？";
      break;
    
    default:
      var str = "続行してよろしいですか？";
      break;
  }

  return confirm(str);

}
