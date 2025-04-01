var height = 0;
if ($(".navbar-notification").length > 0) {
    height = $(".navbar-notification").outerHeight() + $(".navbar").outerHeight();
    var isScrolled = !0
} else {
    height = $(".navbar").outerHeight();
    isScrolled = !1
}
var prevScrollpos = window.pageYOffset;

function TrasformElementsOnScroll(a = !1) {
    if (isScrolled | a) {
        var t = window.pageYOffset,
            n = $(".navbar-notification").outerHeight();
        prevScrollpos > t ? ($(".navbar-notification").css("transform", "none"), $(".navbar").css("transform", "translateY(" + n + "px)")) : ($(".navbar-notification").css("transform", "translateY(" + -n + "px)"), $(".navbar").css("transform", "none")), prevScrollpos = t
    }
}

function adjustMainOffset() {
    height = $(".navbar").outerHeight(), $("main").css("transform", "translateY(" + height + "px)"), $("footer").css("transform", "translateY(" + height + "px)")
}

function adjustNavbarOffset() {
    $(".navbar").css("transform", $(".navbar-notification").outerHeight() + "px")
}

function DisableLink() {
    $(window).width() <= 768 && $(".nav-stend").attr("href", "#")
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

// == //

function Start() {
    $(".navbar-notification").css("transform", "none");
    n = $(".navbar-notification").outerHeight();
    $(".navbar").css("transform", "translateY(" + n + "px)");
    adjustMainOffset(), adjustNavbarOffset(), DisableLink()
}
$(document).ready(Start), $(document).resize(Start), $(window).scroll(TrasformElementsOnScroll), navbarToggler.onclick = function () {
    $(".nav-link").toggleClass("link-collapse"), $(".dropdown-menu").toggleClass("dropdown-menu-off-shadow")
};

