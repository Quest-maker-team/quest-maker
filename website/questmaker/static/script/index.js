$(document).on("scroll", window, function () {
    if ($(window).scrollTop()>200){
        $(".scroll").show();
    }
    else{
        $(".scroll").hide();
    }
});