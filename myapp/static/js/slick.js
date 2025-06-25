/*
Template Name: Furnitore - Furniture & Interior Template
Author: Pillarix
Author URI: https://wrapbootstrap.com/user/pillarix
Version: 1.0
*/
/*
-- Slick Three Slider
-- Slick One Slider
-- Variable Product Slider
*/

(function($) {
    "use strict";

    // Slick Three Slider
    $('.three-slider').slick({
        dots: true,
        infinite: false,
        speed: 300,
        slidesToShow: 3,
        slidesToScroll: 3,
        autoplay: true,
        responsive: [{
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });

    // Slick One Slider
    $('.one-slider').slick({
        dots: true,
        infinite: false,
        speed: 300,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true
    });

    // Variable Product Slider
    $(".big-img").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: ".small-img",
    });
    $(".small-img").slick({
        slidesToShow: 5,
        slidesToScroll: 1,
        asNavFor: ".big-img",
        dots: false,
        centerMode: true,
        focusOnSelect: true,
        centerPadding: "5px",
    });

})(window.jQuery);