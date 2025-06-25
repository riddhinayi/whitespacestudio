/*
Template Name: Furnitore - Furniture & Interior Template
Author: Pillarix
Author URI: https://wrapbootstrap.com/user/pillarix
Version: 1.0
*/
/*
-- Page Loading
-- Count Down Date
-- Back To Top
-- AOS Animation 
-- Quantity Button
*/

(function($) {
    "use strict";

    // Page Loading
    document.addEventListener('DOMContentLoaded', function() {
        const preloader = document.querySelector('.page-loading');
        if (preloader) {
            function removePreloader() {
                preloader.classList.remove('active');
                setTimeout(function() {
                    preloader.remove();
                }, 1500);
            }
            removePreloader();
        }
    });
    
    // Count Down Date
    document.addEventListener("DOMContentLoaded", function() {
        var daysElement = document.getElementById("days");
        var hoursElement = document.getElementById("hours");
        var minutesElement = document.getElementById("minutes");
        var secondsElement = document.getElementById("seconds");
        var countdownElement = document.getElementById("countdown");
    
        if (!daysElement || !hoursElement || !minutesElement || !secondsElement || !countdownElement) {
            return;
        }
    
        var countDownDate = new Date("Jan 1, 2025 00:00:00").getTime();
        var x = setInterval(function() {
            var now = new Date().getTime();
            var distance = countDownDate - now;
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
            daysElement.innerHTML = days;
            hoursElement.innerHTML = hours;
            minutesElement.innerHTML = minutes;
            secondsElement.innerHTML = seconds;
    
            if (distance < 0) {
                clearInterval(x);
                countdownElement.innerHTML = "EXPIRED";
            }
        }, 1000);
    });

    // Back To Top
    var backButton = document.createElement("button");
    backButton.id = "back-to-top";
    backButton.title = "Go to top";
    backButton.textContent = "Top";
    document.body.appendChild(backButton);
    window.onscroll = function() {
        scrollFunction();
    };
    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            backButton.style.display = "block";
        } else {
            backButton.style.display = "none";
        }
    }
    backButton.onclick = function() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    };

    // AOS Animation
    AOS.init();
    AOS.refresh();

    // Quantity Button
    document.addEventListener('DOMContentLoaded', function() {
        const productRows = document.querySelectorAll('.product-row');
        productRows.forEach(function(row) {
            const quantityInput = row.querySelector('.quantity-input');
            const decrementBtn = row.querySelector('.decrement-btn');
            const incrementBtn = row.querySelector('.increment-btn');
            decrementBtn.addEventListener('click', function() {
                decrementQuantity(quantityInput);
            });
            incrementBtn.addEventListener('click', function() {
                incrementQuantity(quantityInput);
            });
        });

        function decrementQuantity(input) {
            let currentQuantity = parseInt(input.value, 10);
            if (currentQuantity > 1) {
                input.value = currentQuantity - 1;
            }
        }

        function incrementQuantity(input) {
            let currentQuantity = parseInt(input.value, 10);
            input.value = currentQuantity + 1;
        }
    });


})(window.jQuery);