jQuery(document).ready(function ($) {
    //var scale = 'scale(1)';
    //document.body.style.msTransform = scale;
    htmlWidth = $('html').innerWidth();
    console.log(htmlWidth);
    var w = $(window).width(),
        h = $(window).height();

    console.log("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
    console.log(w);
    console.log(h);

    var w2 = $(window).innerWidth(),
        h2 = $(window).innerHeight();

    console.log("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
    console.log(w2);
    console.log(h2);
    var target_1 = $('bk-plot-layout').length;
    //var len_1 = target_1.length();
    //target_1.
    //console.log(len_1);
    //.getElementsByClassName('bk-plot-wrapper');
    //var target_2 = target_1.length().getElementsByClassName('bk-plot-wrapper');
    console.log(target_1);
    if (target_1) {
        console.log("**************************");
        console.log(target_1);

    }

    var target_3 = $('bk-layout-fixed').length;
    //var len_1 = target_1.length();
    //target_1.
    //console.log(len_1);
    //.getElementsByClassName('bk-plot-wrapper');
    //var target_2 = target_1.length().getElementsByClassName('bk-plot-wrapper');
    console.log(target_3);
    if (target_3) {
        console.log("**************************");
        console.log(target_3);

    }

    var target_4 = $('mainplothahahahahahhahahahahaha').length;
    //var len_1 = target_1.length();
    //target_1.
    //console.log(len_1);
    //.getElementsByClassName('bk-plot-wrapper');
    //var target_2 = target_1.length().getElementsByClassName('bk-plot-wrapper');
    console.log(target_4);
    if (target_4) {
        console.log("**************************");
        console.log(target_4);

    }

    var target_5 = $('bk-plot-layout  bk-layout-fixed mainplothahahahahahhahahahahaha').length;
    //var len_1 = target_1.length();
    //target_1.
    //console.log(len_1);
    //.getElementsByClassName('bk-plot-wrapper');
    //var target_2 = target_1.length().getElementsByClassName('bk-plot-wrapper');
    console.log(target_5);
    if (target_5) {
        console.log("**************************");
        console.log(target_5);

    }

    var target_6 = $('bk-canvas').length;
    //var len_1 = target_1.length();
    //target_1.
    //console.log(len_1);
    //.getElementsByClassName('bk-plot-wrapper');
    //var target_2 = target_1.length().getElementsByClassName('bk-plot-wrapper');
    console.log(target_6);
    if (target_6) {
        console.log("**************************");
        console.log(target_6);

    }
    


    var target_2 = $('bk-plot-wrapper').length;
    console.log(target_2);

    if (target_2) {
        console.log("**************************");
        console.log(target_2);
        console.log(target_2.toString())
        //JSON.stringify(target_2)
        target_2.css('width', '200px');
    }
    //getElementsByClassName('bk-plot-wrapper')[0].getElementsByClassName('bk-canvas-wrapper')[0];
    //document.getElementsByTagName("canvas")[0].style.width = 200;
});