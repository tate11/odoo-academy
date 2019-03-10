// in file academy_tests.js
odoo.define('academy_tests.QuestionKanbanView', function(require) {
    "use strict";

    var KanbanRecord = require('web.KanbanRecord');

    /*
    * Captures question kanban click event when target is the menu button and
    * prevents default code exetution.
    */
    KanbanRecord.include({

        events: _.defaults({
            'click .o_question_kanban_status_bar': '_onKanbanStatusMenuClick',
            'click #question_kanban_status_menu_add_to_test': '_onKanbanStatusMenuAddToTest',
            'click a[data-markdown]': '_onKanbanDataMarkdown',
        }, KanbanRecord.prototype.events),

        _onKanbanStatusMenuClick: function(event) {
            event.preventDefault();
        },

        _onKanbanStatusMenuAddToTest: function(event) {
            var self = this;
            var data = this.recordData;

            event.preventDefault();

            console.log({'default_question_ids': [(4, data['id'])]});

            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'academy.tests.question.append.wizard',
/*                res_id: id,*/
                views: [[false, 'form']],
                target: 'new',
                context: {'default_question_ids': [(4, data['id'])]}
            });

        },

        _onKanbanDataMarkdown: function (event) {
            var self = this;
            var data = this.recordData;

            event.preventDefault();

            try {
                var text = jQuery(event.target).data('markdown');
                self._copyStringToClipboard(text);
            } catch(err) {
                console.log('Markdown could no be copied to clipboard')
            }

        },

        _copyStringToClipboard: function (str) {
           var el = document.createElement('textarea');
           el.value = str;
           el.setAttribute('readonly', '');
           el.style = {position: 'absolute', left: '-9999px'};
           document.body.appendChild(el);
           el.select();
           document.execCommand('copy');
           document.body.removeChild(el);
        },

    });

});


        /*_openRecord: function () {
            this._super.apply(this, arguments);
        },

        _onGlobalClick: function (event) {
            console.log(event);
            this._super.apply(this, arguments);
        },*/
