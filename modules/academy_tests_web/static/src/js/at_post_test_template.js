$(document).ready(function(){

    $('head').append('<link rel="stylesheet" type="text/css" href="/academy_tests_web/static/src/css/at_post_test_template.css">');
});


odoo.define('academy_tests_web.service', function (require) {

    var utils = require('web.utils');
    var Model = require('web.Model');
    var core = require('web.core');
    var website = require('website.website'); // The important line
    var session = require('web.session');

    /* bind double click and single click separately */
    var DELAY = 250, clicks = 0, timer = null;
    var QWeb = core.qweb;


    /*-- Question class
    ------------------------------------------------------------------------*/
    var AtQuestion = core.Class.extend({
        obj : null,

        /** Main class methods
        ---------------------------------------------------------------------*/

        init : function(at_question) {
            /*-- STEP 1: Initialice this object variables -- */
            obj = this;

            obj.bind_events(at_question);

        },

        bind_events : function(at_question) {
            /*-- STEP 2: Initialice Bootstrap javascript elements -- */
            jQuery(at_question).find('[data-toggle="popover"]').popover({container: 'body'});

            /*-- STEP 2: Bind button events --
                 not needed for impugment and information buttons*/
            jQuery(at_question).find('.btn-edit-question').on("click", obj.on_btn_edit_question_click);
            jQuery(at_question).find('.btn-revise-question').on("click", obj.on_btn_revise_question_click);
            jQuery(at_question).find('.btn-revise-question').on("dblclick", obj.on_btn_revise_question_dblclick);

            jQuery(at_question).find('a.ir-attachment-image-datas').on("click", obj.on_ir_attachment_image_datas);

            jQuery(at_question).find('.btn-edit-question-backend').on("click", obj.on_btn_edit_question_backend);
            jQuery(at_question).find('.btn-edit-question-discard').on("click", obj.on_btn_edit_question_discard);
            jQuery(at_question).find('.btn-edit-question-save').on("click", obj.on_btn_edit_question_save);
            jQuery(at_question).find('.btn-edit-question-close').on("click", obj.on_btn_edit_question_discard);

        },

        requery : function (at_question_id, mode) {

            values = {'at_question_id': at_question_id, mode};
            ready = session.rpc("/get-question", values).then(function (result) {

                    /* STEP 2: Get question LI DOM item */
                    at_question = jQuery('#at-question-' + at_question_id);

                    /* STEP 3: Get parent */
                    swap_area = jQuery(at_question);
                    json = JSON.parse(result);
                    jQuery(swap_area).html(json['html']);
                    console.log(json);

                    /* STEP 4: bind events of the new items */
                    obj.bind_events(at_question);

            });
        },



        /** Button events
        ---------------------------------------------------------------------*/

        on_btn_edit_question_click : function(e) {
            self = this;

            /* STEP 1: Get ID stored in a button DATA attribute  */
            at_question_id = jQuery(self).data('question-id');

            obj.requery(at_question_id, 'edit');
        },

        on_btn_revise_question_click : function(e) {
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
        },

        on_btn_revise_question_dblclick : function(e) {
             e.preventDefault();  //cancel system double-click event
        },

        on_ir_attachment_image_datas : function(e) {
            console.log('hola');

            modal = jQuery('#at-post-test-image-zoom')
            span = modal.find('span.at-question-ir-attachment-image')
            img = modal.find('img.at-question-ir-attachment-image')

            src = jQuery(this).attr('href');
            title = jQuery(this).attr('title');

            span.text(title);
            img.attr('src', src);
            img.attr('alt', title);
            img.attr('title', title);

            modal.modal('show');

            e.preventDefault();  //cancel system double-click event
        },

        on_btn_edit_question_backend : function(e) {

            /* STEP 1: Get ID stored in a button DATA attribute  */
            at_question_id = jQuery(self).data('question-id');

            /* STEP 2: Get question LI DOM item */
            at_question = jQuery('#at-question-' + at_question_id);

            new Model('ir.model.data').call('get_object_reference', ['academy_tests', 'action_questions_act_window']).then(function(action_id) {
                action_id = action_id[1];

                /** --- THIS MUST BE CHANGED ---**/
                url = 'http://localhost:30090/web#id=' + at_question_id + '&view_type=form&model=at.question&menu_id=128&action=' + action_id;
                window.open(url, 'backend').focus();

                obj.requery(at_question_id, 'show');

            });
        },

        on_btn_edit_question_discard : function(e) {

            self = this;

            /* STEP 1: Get ID stored in a button DATA attribute  */
            at_question_id = jQuery(self).data('question-id');

            obj.requery(at_question_id, 'show');
        },

        on_btn_edit_question_save : function(e) {

            /* STEP 1: Get ID stored in a button DATA attribute  */
            at_question_id = jQuery(this).data('question-id');

            /* STEP 2: Get question LI DOM item */
            at_question = jQuery('#at-question-' + at_question_id);

            values = obj.get_data(at_question, at_question_id);

            /* --- PERHAPS THIS SHOULD BE TROUGHT THE CONTROLLER ---*/
            new Model('at.question').call('write', [[at_question_id], values]).done(function(result) {
                console.log(result);
            }).always(function(result) {
                if (result != true) {
                    window.alert(JSON.stringify(result));
                } else {
                    obj.requery(at_question_id, 'show');
                };

            });
        },

        get_data : function (li_obj, question_id) {
            var values = {
                'question_id': question_id,
                'name': li_obj.find('.at-question-name').val(),
                'preamble': li_obj.find(".at-question-preamble").val(),
                'description': li_obj.find('.at-question-description').val(),
                'at_answer_ids': []
            }
            console.log(li_obj.find('.at-answer'));
            li_obj.find('.at-answer').each(function(i){
                id = $(this).data('id');
                name = $(this).find('.at-answer-name').val();
                checked = $(this).find('input[type=checkbox]').prop('checked');
                values['at_answer_ids'].push([1, id, {'name': name, 'is_correct': checked }]);
            });
            console.log(values['at_answer_ids']);
            return values;
        }
    });


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

        /*-- STEP 4: Diseble send button --*/
        $('#at-post-test-inpugnment-modal .at-question-send').prop('disabled', true);
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

    /* Inpugnment modal disable send
    -------------------------------------------------------------------------*/

    $('#at-post-test-inpugnment-modal .at-question-inpugment-name').on('input', function() {
        len = jQuery(this).val().length
        $('#at-post-test-inpugnment-modal .at-question-send').prop('disabled', len <= 0);
    });

    jQuery('.at-question').each(function(i, val){new AtQuestion(val); })
});

