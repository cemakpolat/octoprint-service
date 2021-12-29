/*!  Plugin: ssMenu (Sticky Side Navigation)
 *   Author: Asif Mughal
 *   URL: www.codehim.com
 *   License: MIT License
 *   Copyright (c) 2019 - Codehim
 */
/* File: jquery.ss.emenu.js */
(function ($) {
    $.fn.ssMenu = function (options) {

        var setting = $.extend({
            theme: "default", //put the name of theme in string       
            hideOnScroll: false, //true to hide menu while scroll down 
            autoPanelClose: true,
            additionalCSS: ({
                'background': '', //custom background color
                'color': '', //custom text color 
                'boxShadow': '', //to add box shadow 
                'textShadow': '', //to add text shadow 
            }),

        }, options);

        return this.each(function () {

            var target = $(this);
            var ssMenu = $(".ss-menu");
            var Triggers = $(ssMenu).find("li");

            //Applying customizations 

            $(target).addClass(setting.theme);

            $(target).css(setting.additionalCSS);

            $(Triggers).mouseenter(function () {

                if ($(ssMenu).hasClass("open")) {
                    return;
                }
                $(ssMenu).addClass("open");
            });

            $(Triggers).click(function () {
                if ($(ssMenu).hasClass("open") && setting.autoPanelClose) {
                    $(ssMenu).removeClass("open");
                }

            });


            $(window).click(function (e) {
                if ($(e.target).closest(Triggers).length) {
                    return;
                }
                $(ssMenu).removeClass("open");
            });

            if (setting.hideOnScroll == true) {
                $(window).scroll(function () {

                    if ($(this).scrollTop() > 50) {
                        $(ssMenu).removeClass("show").addClass("hide");
                    } else {
                        $(ssMenu).removeClass("hide").addClass("show");
                    }
                });
            }

        });
    };

})(jQuery);