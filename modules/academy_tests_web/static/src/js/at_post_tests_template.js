$(document).ready(function(){

    $('head').append('<link rel="stylesheet" type="text/css" href="/academy_tests_web/static/src/css/at_post_tests_template.css">');

    $('.table-responsive').on('show.bs.dropdown', function () {
         $('.table-responsive').css( "overflow", "inherit" );
    });

    $('.table-responsive').on('hide.bs.dropdown', function () {
         $('.table-responsive').css( "overflow", "auto" );
    });

});
