/*! =========================================================
 *
 * Light Bootstrap Dashboard PRO - V1.3.0
 *
 * =========================================================
 *
 * Copyright 2016 Creative Tim
 * Available with purchase of license from http://www.creative-tim.com/product/light-bootstrap-dashboard-pro
 *
 *                       _oo0oo_
 *                      o8888888o
 *                      88" . "88
 *                      (| -_- |)
 *                      0\  =  /0
 *                    ___/`---'\___
 *                  .' \\|     |// '.
 *                 / \\|||  :  |||// \
 *                / _||||| -:- |||||- \
 *               |   | \\\  -  /// |   |
 *               | \_|  ''\---/''  |_/ |
 *               \  .-\__  '-'  ___/-. /
 *             ___'. .'  /--.--\  `. .'___
 *          ."" '<  `.___\_<|>_/___.' >' "".
 *         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
 *         \  \ `_.   \_ __\ /__ _/   .-` /  /
 *     =====`-.____`.___ \_____/___.-`___.-'=====
 *                       `=---='
 *
 *     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 *
 *               Buddha Bless:  "No Bugs"
 *
 * ========================================================= */

var searchVisible = 0;
var transparent = true;

var transparentDemo = true;
var fixedTop = false;

var mobile_menu_visible = 0,
    mobile_menu_initialized = false,
    toggle_initialized = false,
    bootstrap_nav_initialized = false,
    $sidebar,
    isWindows;

(function(){
    isWindows = navigator.platform.indexOf('Win') > -1 ? true : false;

    if (isWindows && !$('body').hasClass('sidebar-mini')){
       // if we are on windows OS we activate the perfectScrollbar function
       $('.sidebar .sidebar-wrapper, .main-panel').perfectScrollbar();

       $('html').addClass('perfect-scrollbar-on');
   } else {
       $('html').addClass('perfect-scrollbar-off');
   }
})();

$(document).ready(function(){


//Weunion scripts

    $(document).ready(function() {
        var more_than = gettext('Please enter more than');
        var less_than = gettext('Please enter less than');
        var characters = gettext('characters');
        var empty_field = gettext('Field is empty, please fill it.');

    // override jquery validate plugin defaults
    $.validator.setDefaults({
    highlight: function(element) {
        $(element).closest('.form-group').addClass('has-error');
    },
    unhighlight: function(element) {
        $(element).closest('.form-group').removeClass('has-error');
    },
    success: function(element) {
            $(element).closest('.form-group').removeClass('has-error').addClass('has-success');
            },
    errorElement: 'span',
    errorClass: 'help-block',
    errorPlacement: function(error, element) {
        if(element.parent('.input-group').length) {
            error.insertAfter(element.parent());
        } else {
            error.insertAfter(element);
        }
        }
    });
    //Forms validate
        //Validate idea add
        $("#addIdea").validate({
            rules: {
                title: {
                    required: true,
                    maxlength: 255,
                    minlength: 6
                },
                perinfo:"required",

                text: {
                    required: true,
                    minlength: 20,
                    maxlength: 1000
                }
            },
            messages: {
                title:{
                    required: empty_field,
                    maxlength: less_than+' 255 '+ characters+'.',
                    minlength: more_than+ ' 6 ' + characters+'.'
                },
                text: {
                    required: empty_field,
                    maxlength: less_than+' 1000 '+ characters+'.',
                    minlength: more_than+ ' 20 ' + characters+'.'
                },
                perinfo: gettext("Please, read the rules, and confirt that you agree to processing of personal data.")
                    // "Будь ласка, ознайомтесь з правилами модулю 'Ідеї' та підтвердіть, що даєте згоду на обробку персональних даних. "
            }

        });

          //Validate defect add
        $("#addDefect").validate({
            rules: {
                title: {
                    required: true,
                    maxlength: 255,
                    minlength: 10
                },
                description: {
                    required: true,
                    maxlength: 2048,
                    minlength: 10
                },
                address:"required",

            },
            messages: {
                title:{
                    required: empty_field,
                    maxlength: less_than+' 255 '+ characters+'.',
                    minlength: more_than+ ' 10 ' + characters+'.',
                },
                description: {
                    required: empty_field,
                    maxlength:less_than+' 2048 '+ characters+'.',
                    minlength: more_than+ ' 10 ' + characters+'.',
                },
                address: {
                    required: empty_field,
                }

            }

        });
    // Valifate phone number in signupform
        $.validator.addMethod('customphone', function (value, element) {
            return this.optional(element) || /^\+?\d[\d\(?\)?\s-]{0,18}$/.test(value);
        }, gettext("Please enter a valid phone number"));

     //Validate defect add
        $("#signupform").validate({
            rules: {
                email: {
                    required: true,
                    maxlength: 254,
                    minlength: 5,
                    email: true
                },
                first_name: {
                    required: true,
                    maxlength: 30,
                    minlength: 2
                },

                last_name: {
                    required: true,
                    maxlength: 30,
                    minlength: 2
                },
                middle_name: {
                    required: true,
                    maxlength: 30,
                    minlength: 2
                },
                condominiums: "required",
                phone: {
                    required: true,
                    customphone: true,
                    maxlength: 50,
                    minlength: 5

                },
                password2: {
                    required: true,
                    maxlength: 40,
                    minlength: 6
                },
                password1: {
                    required: true,
                    maxlength: 40,
                    minlength: 6,
                    equalTo : "#id_password2"
                },
                perinfo:"required",
            },
            messages: {
                email:{
                    required: empty_field,
                    maxlength: less_than+' 254 '+ characters+'.',
                    minlength: more_than+ ' 5 ' + characters+'.',
                    email: gettext("Please enter valid e-mail")
                },
                first_name: {
                    required: empty_field,
                    maxlength: less_than+' 30 '+ characters+'.',
                    minlength: more_than+ ' 2 ' + characters+'.',
                },
                last_name: {
                    required: empty_field,
                    maxlength: less_than+' 30 '+ characters+'.',
                    minlength: more_than+ ' 2 ' + characters+'.',
                },
                middle_name: {
                    required: empty_field,
                    maxlength: less_than+' 30 '+ characters+'.',
                    minlength: more_than+ ' 2 ' + characters+'.',
                },
                phone: {
                    required: empty_field,
                    maxlength: less_than+' 50 '+ characters+'.',
                    minlength: more_than+ ' 5 ' + characters+'.',
                },
                password2: {
                    required: empty_field,
                    maxlength: less_than+' 40 '+ characters+'.',
                    minlength: more_than+ ' 6 ' + characters+'.',
                },
                password1: {
                    required: empty_field,
                    maxlength: less_than+' 40 '+ characters+'.',
                    minlength: more_than+ ' 6 ' + characters+'.',
                    equalTo: gettext("Password must be equal to the previous")
                },
                condominiums: {
                    required: empty_field
                },
                perinfo: gettext("Please enter your first name, middle name, last name, phone, password and condominium")
            }
        });

          //Validate defect add
        $("#newsform").validate({
            rules: {
                title: {
                    required: true,
                    maxlength: 150,
                    minlength: 10
                },
                shortdesc: {
                    required: true,
                    maxlength: 300,
                    minlength: 10
                },
                text:"required",

            },
            messages: {
                title:{
                    required: empty_field,
                    maxlength: less_than+' 150 '+ characters+'.',
                    minlength: more_than+ ' 10 ' + characters+'.',
                },
                shortdesc: {
                    required: empty_field,
                    maxlength: less_than+' 300 '+ characters+'.',
                    minlength: more_than+ ' 10 ' + characters+'.',
                },
                text: {
                    required: empty_field,
                }
            }
        });


           //Validate Defects Fix Status
        $("#defcomments").validate({
            rules: {
                body:"required",
            },
            messages: {
                body: {
                    required: empty_field,

                },
            }
        });

         //Validate Defects Fix Status
        $("#reason").validate({
            rules: {
                description:"required"
            },
            messages: {
                description: {
                    required: empty_field

                }
            }
        });

      //Validate loginform
        $("#loginform").validate({
            rules: {

                login: {
                    required: true,
                    maxlength: 254,
                    minlength: 5,
                    email: true
                },
                password:{
                    required: true,
                    maxlength: 40,
                    minlength: 3
                },

            },
            messages: {
                login:{
                    required: empty_field,
                    maxlength: less_than+' 254 '+ characters+'.',
                    minlength: more_than+ ' 5 ' + characters+'.',
                    email: gettext("Please enter valid e-mail")
                },
                password: {
                    required: empty_field,
                    maxlength: less_than+' 40 '+ characters+'.',
                    minlength: more_than+ ' 3 ' + characters+'.'

                },
            }
        });

      mvsWantedValidate($('#addMvsWanted'));
      initForm($('#addMvsWanted'));

      mvsWantedValidate($('#editMvsWanted'));
      initForm($('#editMvsWanted'));

     $.validator.addMethod("dateFormat",
        function(value, element) {
                return value.match(/^\d\d?\/\d\d?\/\d\d\d\d$/);
    },
    gettext("Enter date in format: dd/mm/yyyy.")
     );
});

function initForm(form) {
  form.on('submit', function () {
    if (!form.valid()) {
      return false;
    }
    var button = form.find('input[type=submit]');
    button.val('Submit ..');
    button.attr('disabled', 'disabled');
    this.submit();
    return true;
  });
}

function mvsWantedValidate(form) {
        var more_than = gettext('Please enter more than');
        var less_than = gettext('Please enter less than');
        var characters = gettext('characters');
        var empty_field = gettext('Field is empty, please fill it.');
        form.validate({
            rules: {
                name: {
                    required: true,
                    maxlength: 255,
                    minlength: 10
                },
                birth_date: {
                    required: true,
                    dateFormat: true
                },
                text: {
                    required: true,
                    maxlength: 2000,
                    minlength: 20
                }
            },
            messages: {
                name:{
                    required: empty_field,
                    maxlength: less_than+' 255 '+ characters+'.',
                    minlength: more_than+ ' 10 ' + characters+'.',
                },
                birth_date:{
                    required: empty_field,
                },
                text: {
                    required: empty_field,
                    maxlength: less_than+' 2000 '+ characters+'.',
                    minlength: more_than + ' 20 ' + characters+'.',
                }
            }
        });
}

    //Validate status changer
        $(".changestatus").validate({
            rules: {
                resolution:"required"
            },
            messages: {
                resolution: gettext("Please use valid status")
            }
        });





function printPage() {
    window.print();
}

$('.condominium').click(function () {
  $('.condominium').hide();
  $('.chooseacondominium .fa').hide();
  $('#livesearch').show();
  $('#livesearch input').focus();

})

$('#livesearch .fa').click(function () {
  $('.condominium').show();
  $('.chooseacondominium .fa').show();
  $('#livesearch').hide();
})

var options = {
    url: "http://"+window.location.hostname+(window.location.port.length>1?":"+window.location.port:"")+"/condominiumslivesearch/",
    //EmptyMessage: "������� ��������� ����� ������� � ����� ���. ������?",
    getValue: "name",
    list: {
          showAnimation: {
              type: "fade", //normal|slide|fade
              time: 400,
              callback: function() {}
          },

          hideAnimation: {
              type: "fade", //normal|slide|fade
              time: 400,
              callback: function() {}
          },
          maxNumberOfElements: 10,
          sort: {
                enabled: true
            },
          match: {
                enabled: true
            }
      },
    template: {
        type: "custom",
        method: function(value, item) {
            return "<a href='/choosecondominium/"+ item.id + "'>"+item.type+" <strong>"+item.name+"</strong></a><small> ("+item.gromada+"" + item.region+")</small>";
        }
    }
};


$(".easy-autocomplete-container li div small").click(function(){

    console.log("Click");
    link = $(".easy-autocomplete-container .selected a").attr("href");
    location.href = link;

});


e=$(".easy-autocomplete-container .selected a").attr("href")



    window_width = $(window).width();
    $sidebar = $('.sidebar');

    // check if there is an image set for the sidebar's background
    lbd.checkSidebarImage();

    if($('body').hasClass('sidebar-mini')){
        lbd.misc.sidebar_mini_active = true;
    }

    lbd.initSidebarsCheck();

    lbd.initMinimizeSidebar();

    $('.form-control').on("focus", function(){
        $(this).parent('.input-group').addClass("input-group-focus");
    }).on("blur", function(){
        $(this).parent(".input-group").removeClass("input-group-focus");
    });

    // Init Collapse Areas
    lbd.initCollapseArea();

    // Init Tooltips
    $('[rel="tooltip"]').tooltip();

    // Init Tags Input
    if($(".tagsinput").length != 0){
        $(".tagsinput").tagsInput();
    }

    //  Init Bootstrap Select Picker
    if($(".selectpicker").length != 0){
        $(".selectpicker").selectpicker();
    }

});

// activate mobile menus when the windows is resized
$(window).resize(function(){
    lbd.initSidebarsCheck();
});


lbd = {

    misc:{
        navbar_menu_visible: 0,
        active_collapse: true,
        disabled_collapse_init: 0,

    },

    checkSidebarImage: function(){
        $sidebar = $('.sidebar');
        image_src = $sidebar.data('image');

        if(image_src !== undefined){
            sidebar_container = '<div class="sidebar-background" style="background-image: url(' + image_src + ') "/>'
            $sidebar.append(sidebar_container);
        } else if(mobile_menu_initialized == true){
            // reset all the additions that we made for the sidebar wrapper only if the screen is bigger than 991px
            $sidebar_wrapper.find('.navbar-form').remove();
            $sidebar_wrapper.find('.nav-mobile-menu').remove();

            mobile_menu_initialized = false;
        }
    },

    initSidebarsCheck: function(){
        if($(window).width() <= 991){
            if($sidebar.length != 0){
                lbd.initSidebarMenu();

            } else {
                lbd.initBootstrapNavbarMenu();
            }
        }

    },

    initMinimizeSidebar: function(){

        // when we are on a Desktop Screen and the collapse is triggered we check if the sidebar mini is active or not. If it is active then we don't let the collapse to show the elements because the elements from the collapse are showing on the hover state over the icons in sidebar mini, not on the click.
        $('.sidebar .collapse').on('show.bs.collapse',function(){
            if($(window).width() > 991){
                if(lbd.misc.sidebar_mini_active == true){
                    return false;
                } else{
                    return true;
                }
            }
        });

        $('#minimizeSidebar').click(function(){
            var $btn = $(this);

            if(lbd.misc.sidebar_mini_active == true){
                $('body').removeClass('sidebar-mini');
                lbd.misc.sidebar_mini_active = false;

                if(isWindows){
                    $('.sidebar .sidebar-wrapper').perfectScrollbar();
                }

            }else{

                $('.sidebar .collapse').collapse('hide').on('hidden.bs.collapse',function(){
                    $(this).css('height','auto');
                });

                if(isWindows){
                    $('.sidebar .sidebar-wrapper').perfectScrollbar('destroy');
                }

                setTimeout(function(){
                    $('body').addClass('sidebar-mini');

                    $('.sidebar .collapse').css('height','auto');
                    lbd.misc.sidebar_mini_active = true;
                },300);
            }

            // we simulate the window Resize so the charts will get updated in realtime.
            var simulateWindowResize = setInterval(function(){
                window.dispatchEvent(new Event('resize'));
            },180);

            // we stop the simulation of Window Resize after the animations are completed
            setTimeout(function(){
                clearInterval(simulateWindowResize);
            },1000);
        });
    },


    checkFullPageBackgroundImage: function(){
        $page = $('.full-page');
        image_src = $page.data('image');

        if(image_src !== undefined){
            image_container = '<div class="full-page-background" style="background-image: url(' + image_src + ') "/>'
            $page.append(image_container);
        }
    },

    initSidebarMenu: debounce(function(){
        $sidebar_wrapper = $('.sidebar-wrapper');

        //console.log('aici se face meniu in dreapta');

        if(!mobile_menu_initialized){

            $navbar = $('nav').find('.navbar-collapse').first().clone(true);

            nav_content = '';
            mobile_menu_content = '';

            //add the content from the regular header to the mobile menu
            //pas = 1;
            $navbar.children('ul').each(function(){

                content_buff = $(this).html();
                nav_content = nav_content + content_buff;
                //console.log('pas:' + pas);

                //pas = pas+1;
            });

            nav_content = '<ul class="nav nav-mobile-menu">' + nav_content + '</ul>';

            $navbar_form = $('nav').find('.navbar-form').clone(true);

            $sidebar_nav = $sidebar_wrapper.find(' > .nav');

            // insert the navbar form before the sidebar list
            $nav_content = $(nav_content);
            $nav_content.insertBefore($sidebar_nav);
            $navbar_form.insertBefore($nav_content);

            $(".sidebar-wrapper .dropdown .dropdown-menu > li > a").click(function(event) {
                event.stopPropagation();

            });

            mobile_menu_initialized = true;
        } else {
            console.log('window with:' + $(window).width());
            if($(window).width() > 991){
                // reset all the additions that we made for the sidebar wrapper only if the screen is bigger than 991px
                $sidebar_wrapper.find('.navbar-form').remove();
                $sidebar_wrapper.find('.nav-mobile-menu').remove();

                console.log(lbd.misc.sidebar_mini_active);

                // if(lbd.misc.sidebar_mini_active == true){
                //     $('body').addClass('sidebar-mini');
                // }

                mobile_menu_initialized = false;
            }
        }

        if(!toggle_initialized){
            $toggle = $('.navbar-toggle');

            $toggle.click(function (){

                if(mobile_menu_visible == 1) {
                    $('html').removeClass('nav-open');

                    $('.close-layer').remove();
                    setTimeout(function(){
                        $toggle.removeClass('toggled');
                    }, 400);

                    mobile_menu_visible = 0;
                } else {
                    setTimeout(function(){
                        $toggle.addClass('toggled');
                    }, 430);


                    main_panel_height = $('.main-panel')[0].scrollHeight;
                    $layer = $('<div class="close-layer"></div>');
                    $layer.css('height',main_panel_height + 'px');
                    $layer.appendTo(".main-panel");

                    setTimeout(function(){
                        $layer.addClass('visible');
                    }, 100);

                    $layer.click(function() {
                        $('html').removeClass('nav-open');
                        mobile_menu_visible = 0;

                        $layer.removeClass('visible');

                         setTimeout(function(){
                            $layer.remove();
                            $toggle.removeClass('toggled');

                         }, 400);
                    });

                    $('html').addClass('nav-open');
                    mobile_menu_visible = 1;

                }
            });

            toggle_initialized = true;
        }
    }, 500),


    initBootstrapNavbarMenu: debounce(function(){

        if(!bootstrap_nav_initialized){
            $navbar = $('nav').find('.navbar-collapse').first().clone(true);

            nav_content = '';
            mobile_menu_content = '';

            //add the content from the regular header to the mobile menu
            $navbar.children('ul').each(function(){
                content_buff = $(this).html();
                nav_content = nav_content + content_buff;
            });

            nav_content = '<ul class="nav nav-mobile-menu">' + nav_content + '</ul>';

            $navbar.html(nav_content);
            $navbar.addClass('bootstrap-navbar');

            // append it to the body, so it will come from the right side of the screen
            $('body').append($navbar);

            $toggle = $('.navbar-toggle');

            $navbar.find('a').removeClass('btn btn-round btn-default');
            $navbar.find('button').removeClass('btn-round btn-fill btn-info btn-primary btn-success btn-danger btn-warning btn-neutral');
            $navbar.find('button').addClass('btn-simple btn-block');

            $toggle.click(function (){
                if(mobile_menu_visible == 1) {
                    $('html').removeClass('nav-open');

                    $('.close-layer').remove();
                    setTimeout(function(){
                        $toggle.removeClass('toggled');
                    }, 400);

                    mobile_menu_visible = 0;
                } else {
                    setTimeout(function(){
                        $toggle.addClass('toggled');
                    }, 430);

                    $layer = $('<div class="close-layer"></div>');
                    $layer.appendTo(".wrapper-full-page");

                    setTimeout(function(){
                        $layer.addClass('visible');
                    }, 100);


                    $layer.click(function() {
                        $('html').removeClass('nav-open');
                        mobile_menu_visible = 0;

                        $layer.removeClass('visible');

                         setTimeout(function(){
                            $layer.remove();
                            $toggle.removeClass('toggled');

                         }, 400);
                    });

                    $('html').addClass('nav-open');
                    mobile_menu_visible = 1;

                }

            });
            bootstrap_nav_initialized = true;
        }
    }, 500),

    initCollapseArea: function(){
        $('[data-toggle="collapse-hover"]').each(function () {
            var thisdiv = $(this).attr("data-target");
            $(thisdiv).addClass("collapse-hover");
        });

        $('[data-toggle="collapse-hover"]').hover(function(){
            var thisdiv = $(this).attr("data-target");
            if(!$(this).hasClass('state-open')){
                $(this).addClass('state-hover');
                $(thisdiv).css({
                    'height':'30px'
                });
            }

        },
        function(){
            var thisdiv = $(this).attr("data-target");
            $(this).removeClass('state-hover');

            if(!$(this).hasClass('state-open')){
                $(thisdiv).css({
                    'height':'0px'
                });
            }
        }).click(function(event){
                event.preventDefault();

                var thisdiv = $(this).attr("data-target");
                var height = $(thisdiv).children('.panel-body').height();

                if($(this).hasClass('state-open')){
                    $(thisdiv).css({
                        'height':'0px',
                    });
                    $(this).removeClass('state-open');
                } else {
                    $(thisdiv).css({
                        'height':height + 30,
                    });
                    $(this).addClass('state-open');
                }
            });
    }
}


// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.

function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        }, wait);
        if (immediate && !timeout) func.apply(context, args);
    };
};
