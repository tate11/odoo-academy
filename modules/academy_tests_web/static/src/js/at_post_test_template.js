$(document).ready(function(){

    $('head').append('<link rel="stylesheet" type="text/css" href="/academy_tests_web/static/src/css/at_post_test_template.css">');
});


odoo.define('academy_tests_web.service', function (require) {

    "use strict";

    var utils = require('web.utils');
    var Model = require('web.Model');
    var core = require('web.core');
    var website = require('website.website'); // The important line

    /*var action_manager = new ActionManager(self);*/

    $('*[.btn-edit-question]').click(function () {
        var action = {
            type: 'ir.actions.act_window',
            res_model: 'at.question',
            view_mode: 'form',
            view_type: 'form',
            views: [[false, 'form']],
            target: 'new',
            context: {},
        };

        /*action_manager.do_action(action);*/
    });
});

