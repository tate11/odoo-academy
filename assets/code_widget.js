odoo.define('academy_base.widgets', function (require) {

    "use strict";

    var core = require('web.core');
    var form_common = require('web.form_common');
    var form_relational = require('web.form_relational');
    var Model = require('web.DataModel');
    var utils = require('web.utils');
    var data = require('web.data');
    var QWeb = core.qweb;

    var _t = core._t;



    var FieldMany2ManyClick = form_relational.AbstractManyField.extend({

        template : 'FieldMany2ManyClick',
        tagName : 'div',
        className : 'oe_form_field_many2many_click',

        events: {},
        custom_events : {},
        attributes : {},

        init: function (field_manager, node) {
            this._super(field_manager, node);

            this.records = [];
            this.fields = [
                'name',
                'sequence',
                'overall',
                'done',
                'remaining',
                'overage'
            ];
        },

        start: function() {
            this._super();
            console.log(this.dataset);
        },

        willStart: function() {
            var result = $.Deferred();

            this.records = this.get("value");

            deferred.resolve();

            return jQuery.when(this._super.apply(this, arguments), deferred);
        },

        /*render_value: function () {
            console.log('renderValue');

            console.log(this.get("value"));

            // return this._super.apply(this, arguments);
        },

        query_records: function() {
            console.log('query_records');

            console.log(this);
        },
*/
        renderElement: function() {
            // insert code to execute before rendering, for object initialization
            console.log('renderElement');

            var ids = this.get("value");
            var template = this.template;
            console.log(ids);

            this.$el.html(QWeb.render('FieldMany2ManyClick', {widget: this}));

            return this._super.apply(this, arguments);
        },/*
*/
        destroy : function () {
            this._super.apply(this, arguments);
        },


        delegateEvents: function (events) {
            this._super.apply(this, arguments);
            return this;
        },


        undelegateEvents: function () {
            this._super.apply(this, arguments);
            return this;
        }

    });


    core.form_widget_registry.add('many2many_click', FieldMany2ManyClick);

/*    return {
        FieldMany2OneButtons: FieldMany2OneButtons,
    }*/
});
