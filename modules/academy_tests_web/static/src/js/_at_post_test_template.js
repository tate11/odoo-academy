$(document).ready(function(){

    /* Hide icons for right answers
    -------------------------------------------------------------------------*/

    $('head').append('<link rel="stylesheet" type="text/css" href="/academy_tests_web/static/src/css/at_post_test_template.css">');


    /* Hide icons for right answers
    -------------------------------------------------------------------------*/

    $('.at-post-test-question .fa-check').hide();

    /* Inpugnment modal dialog AJAX behavior
    -------------------------------------------------------------------------*/

    $('#impugnment-modal .btn-primary').click(function() {

        $.ajax({
            url: '/proccess-impugnment',
            type: 'POST',
            dataType: 'html',
            data: {
                csrf_token : $("#csrf_token").val(),
                question_id : $("#question_id").val(),
                name:$("#name").val(),
                description:$("#description").val()
            },
            success: function (data) {
                $('#impugnment-modal').modal('hide');
                $('#impugnment-result-message').html(data);
                $('#impugnment-result-modal').modal('show');
            },
        });

    });


    /* Inpugnment modal dialog AJAX response
    -------------------------------------------------------------------------*/

    $('#impugnment-modal #name').on('input', function() {
        len = jQuery('#impugnment-modal #name').val().length
        $('#impugnment-modal .btn-primary').prop('disabled', len <= 0);
    });

});



function saveQuestion(param) {

    question_id = $(param).data('question-id')
    li_obj = $(param).parent().parent()


    jsondata = {
        'jsonrpc': "2.0",
        'method': "call",
        'csrf_token' : $("#csrf_token").val(),
        "params": {
            'question_id': question_id,
            'name': li_obj.find('#name').val(),
            'preamble': li_obj.find("#preamble").val(),
            'description': li_obj.find('#description').val(),
            'at_answer_ids': []
        }
    };

    li_obj.find('.at-post-test-answer').each(function(i){
        id = $(this).data('id');
        name = $(this).find('#name').val();
        checked = $(this).find('input[type=checkbox]').prop('checked');
        jsondata.params['at_answer_ids'].push([1, id, {'name': name, 'is_correct': checked }]);
    });

    $.ajax({
        url: '/update-question',
        type: 'POST',
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(jsondata),
        success: function (data) {
            discardQuestion(param);
        },
    });

};

function editQuestion(param) {

    question_id = $(param).data('question-id')
    li_obj = $(param).parent().parent()

    $.ajax({
        url: '/get-question',
        type: 'POST',
        dataType: 'html',
        data: {
            csrf_token : $("#csrf_token").val(),
            question_id: question_id,
            edit: 1,
        },
        success: function (data) {
            li_obj.html(data);
        },
    });

};

function discardQuestion(param) {

    question_id = $(param).data('question-id')
    li_obj = $(param).parent().parent()

    $.ajax({
        url: '/get-question',
        type: 'POST',
        dataType: 'html',
        data: {
            csrf_token : $("#csrf_token").val(),
            question_id: question_id,
        },
        success: function (data) {
            li_obj.html(data);
        },
    });

};

function singleClick(e) {
    jQuery(this).parent().parent().find('.fa-check').toggle();
};

function doubleClick(e) {
    visible = jQuery(this).parent().parent().find('.fa-check').is(":visible");
    if (visible == true) {
        jQuery('.at-post-test-question .fa-check').hide();
    } else {
        jQuery('.at-post-test-question .fa-check').show();
    }
};


function showRightAnswer(param) {

    setTimeout(function() {
        var dblclick = parseInt($(param).data('double'), 10);
        if (dblclick > 0) {
            $(param).data('double', dblclick-1);
        } else {
            singleClick.call(param, param);
        }
    }, 300);
};

function showRightAnswers(param) {
    $(param).data('double', 2);
    doubleClick.call(param, param);
};



/* Click behavior to show inpugnment modal dialog
-------------------------------------------------------------------------*/

function showInpugnmentDialog(param) {
    id = jQuery(param).parent().parent().parent().data('question');

    $('#impugnment-form')[0].reset();
    $('#impugnment-modal .btn-primary').prop('disabled', true);

    $('#impugnment-modal #question_id').val(id)
};
