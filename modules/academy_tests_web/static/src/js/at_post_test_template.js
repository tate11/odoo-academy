$(document).ready(function(){

    $('head').append('<link rel="stylesheet" type="text/css" href="/academy_tests_web/static/src/css/at_post_test_template.css">');
});


odoo.define('academy_tests_web.service', function (require) {

    var utils = require('web.utils');
    var Model = require('web.Model');
    var core = require('web.core');
    var website = require('website.website'); // The important line

    /* bind double click and single click separately */
    var DELAY = 250, clicks = 0, timer = null;


    /*-- Enable Popovers
    ------------------------------------------------------------------------*/

    // Contain the popover within the body NOT the element it was called in.
    $('[data-toggle="popover"]').popover({container: 'body'});


    /*-- Impugment modals
    ------------------------------------------------------------------------*/

    $('#at-post-test-inpugnment-modal').on('show.bs.modal', function (e) {
        console.log(e.relatedTarget);

        self = this;

        at_question_id = jQuery(e.relatedTarget).data('question-id');

        /*-- STEP 1: Change modal title --*/
        atqid_span = 'span.at-question-inpugment-at-question-id'
        jQuery(self).find(atqid_span).text(at_question_id);

        /*-- STEP 2: Set token and at_question_id --*/
        token = 'input[name="csrf_token"]'
        csrf_token = $("#csrf_token").val()

        jQuery(self).find(token).val(csrf_token);

        atqid = 'input[name="at-question-inpugment-at-question-id"]';
        jQuery(self).find(atqid).val(at_question_id);

        /*-- STEP 3:  Clear fields --*/
        name = 'input[name="at-question-inpugment-name"]';
        jQuery(self).find(name).val('');

        desc = 'textarea[name="at-question-inpugment-description"]';
        jQuery(self).find(desc).val('');
    })


    jQuery('#at-post-test-inpugnment-modal .at-question-send').click(function() {

        atqid = 'input[name="at-question-inpugment-at-question-id"]';
        name = 'input[name="at-question-inpugment-name"]';
        desc = 'textarea[name="at-question-inpugment-description"]';

        values = {
            'at_question_id' : jQuery(atqid).val(),
            'name' : jQuery(name).val(),
            'description' : jQuery(desc).val(),
        };

        try {
            new Model("at.question.impugnment")
            .call("create", [values])
                .then(function (result) {

                    jQuery('#at-post-test-inpugnment-modal').modal('hide');

                    resm = jQuery('#impugnment-result-modal');
                    msgp = jQuery(resm).find('.impugnment-result-message');

                    jQuery('.impugnment-result-modal-at-question-inpugment-id').text(result);
                    jQuery('.impugnment-result-modal-at-question-id').text(values['at_question_id']);
                    jQuery('.impugnment-result-modal-name').text(values['name']);
                    jQuery('.impugnment-result-modal-description').text(values['description']);

                    jQuery('#impugnment-result-modal').modal('show');

                    $(resm).modal('show');
                });
        }
        catch(err) {
            alert(err);
        }


        console.log(values);
    });

    /*-- Question options toolbar behavior
    ------------------------------------------------------------------------*/

    jQuery('.btn-edit-question').click(function () {
        self = this;
    });

    /*  NOT NEEDED
    jQuery('.btn-describe-question').click(function(){});
    jQuery('.btn-impugn-question').click(function(){});
    */

    jQuery('.btn-revise-question').on("click", function(e){
        self = this;

        clicks++;  //count clicks

        if(clicks === 1) {

            timer = setTimeout(function() {

                /* STEP 1: Get ID stored in a button DATA attribute  */
                at_question_id = jQuery(self).data('question-id');

                /* STEP 2: Get question LI DOM item */
                at_question = jQuery('#at-question-' + at_question_id);

                /* STEP 3: Toggle visibility */
                chksel = '.at-answer-iscorrect-checkmark';
                jQuery(at_question).find(chksel).toggle();

                clicks = 0;             //after action performed, reset counter

            }, DELAY);

        } else {

            clearTimeout(timer);    //prevent single-click action

            /* STEP 1: Get ID stored in a button DATA attribute  */
            id = jQuery(self).data('question-id');

            /* STEP 2: Get question LI DOM item */
            at_question = jQuery('#at-question-' + id);

            /* STEP 3: Check if some answer has the check mark visible */
            chksel = '.at-answer-iscorrect-checkmark:visible';
            is_checked = jQuery(at_question).find(chksel).length > 0;

            /* STEP 4: Change visibility of all check marks in oposite to the
            selected question */
            at_question_ids = jQuery('.at-question-ids')

            if (is_checked == true) {
                visible = jQuery(at_question_ids).find('.at-answer-iscorrect-checkmark').hide();
            } else {
                visible = jQuery(at_question_ids).find('.at-answer-iscorrect-checkmark').show();
            }

            clicks = 0;             //after action performed, reset counter

        }

    })
    .on("dblclick", function(e){
        e.preventDefault();  //cancel system double-click event
    }); /* jQuery('.btn-revise-question') */

});

