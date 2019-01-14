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

    });

});


        /*_openRecord: function () {
            this._super.apply(this, arguments);
        },

        _onGlobalClick: function (event) {
            console.log(event);
            this._super.apply(this, arguments);
        },*/
