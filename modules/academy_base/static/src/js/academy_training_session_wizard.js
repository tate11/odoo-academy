odoo.define("academy_base.form_widgets", function (require) {

    "use strict";

    var core = require("web.core");
    var form_common = require("web.form_common");
    var Model = require("web.DataModel");

    var QWeb = core.qweb;



    var AcademyTrainingActionUnitControlSelector = form_common.FormWidget.extend(form_common.FieldManagerMixin, form_common.ReinitializeWidgetMixin, {

        template: "FieldMany2ManyClick",
        events: {},

        fullrecordset: [],
        extra_rows: [],
        has_ever_been_rendered: false,
        fields: ["sequence", "name", "overall", "done", "remaining", "overage"],


        init: function () {
            var self = this;
            var result = self._super.apply(self, arguments);

            self.do_link_to_action_id();

            return result;
        },


        start: function () {
            var result =  this._super.apply(this, arguments);
            return result;
        },


        renderElement: function () {
            var self = this;
            var result =  self._super.apply(self, arguments);

            //console.log(self);

            if (self.fullrecordset) {
                self.extra_rows = _.range(Math.max(0, 5 - self.fullrecordset.length));

                self.$el.html(QWeb.render(self.template, {widget: self}));
                self.$el.find("tbody tr").on("click", {widget: self}, self._on_row_click);
            }

            return result;
        },


        /**
        * Links this widget to the ``academy_training_action_id`` field from
        * main form, once the field changes this field updates itself.
        */
        do_link_to_action_id: function () {
            this.field_manager.on(
                "field_changed:academy_training_action_id",
                this,
                this.do_requery
            );
        },


        /**
        * Event response, its called when ``academy_training_action_id``
        * (form main form) has been changed.
        */
        do_requery: function () {
            var self = this;
            var promise = this.do_load_data();

            promise.done(function (records) {
                self.renderElement();
                self.do_update_parent();
            });
        },


        do_update_parent: function (){
            var self = this;
            var fm = self.field_manager;
            var base = jQuery(self.$el).find('tbody');

            fm.set_values({'action_unit_control_ids': [[5]]});

            var ids = []
            base.find('tr').each(function (index, item) {
                var selected = jQuery(item).data("selected");
                if (selected === "1") {
                    ids.push(jQuery(item).data("id"));
                }
            });

            fm.set_values({'action_unit_control_ids': [[6, 0, ids]]});

        },


        /**
        * Loads all the ``academy.training.action.unit.control`` records
        * related with choosen ``academy_training_action_id`` value.
        * - All records will be stored in ``this.unit_control_set`` attribute
        * - If ``academy_training_action_id`` is not set, the value for
        * ``this.unit_control_set`` will be en empty array ``[]``
        *
        * @return: method is asynchronous and it returns a jQuery promise.
        */
        do_load_data: function () {

            var self = this;

            var fm = self.field_manager;
            var action_id = fm.get_field_value("academy_training_action_id");

            var deferred = jQuery.Deferred();

            if (action_id !== null && action_id !== undefined) {

                var modelObj = new Model("academy.training.action.unit.control");

                var domain = [
                    ["active", "=", true],
                    ["remaining", ">", 0],
                    ["academy_training_action_id", "=", action_id]
                ];
                var fields = self.fields.concat(["id", "academy_training_unit_id"]);

                modelObj.query(fields).filter(domain).all().then(
                    function (records) {
                        self.fullrecordset = records;
                        deferred.resolve(records);
                    }
                );

            } else {
                self.fullrecordset = [];
                deferred.resolve([]);
            }

            return deferred.promise();

        }, /* do_load_data */

        _get_row_data: function(row) {
            var rowObj = jQuery(row);
            var row_data = {}

            rowObj.find("td[data-field]").each(function( index, tdObj ) {
                var field_name = jQuery(tdObj).data('field');
                var field_value = jQuery(tdObj).data('value');
                row_data[field_name] = field_value;
            });

            /* Not needed
            row_data['data-academy-training-unit-id'] =
                jQuery(rowObj).data('data-academy-training-unit-id');*/
            return [
                1,
                jQuery(rowObj).data('id'),
                row_data
            ];

        }, /* _get_row_data */


        /**
        *   Event response triggerd when user clicks on a row. Performs all
        *   needed actions to mark target row as selected.
        */
        _on_row_click: function (ev) {
            var target = jQuery(ev.currentTarget);
            var self = ev.data.widget;

            /*var id = target.data("id"); -- Not needed */
            var unit_id = target.data("academy-training-unit-id");
            var selected = target.data("selected");


            //var row_data = self._get_row_data(ev.currentTarget);
            //var id = row_data[1];

            if (selected === "1") {
                target.removeData("selected");
                target.removeClass("selected").removeClass("success");
                target.find("i").removeClass("fa-check-square-o").addClass("fa-square-o");
            } else {
                target.data("selected", "1");
                target.addClass("selected").addClass("success");
                target.find("i").removeClass("fa-square-o").addClass("fa-check-square-o");
            }

            self.do_update_parent();

        }


    }); /*-- AcademyTrainingActionUnitControlSelector -- */

core.form_custom_registry.add("unitcontrolselector", AcademyTrainingActionUnitControlSelector);

}); /*-- odoo.define -- */

/*
temp1.field_manager.set_values({'action_unit_control_ids': [[5]]});
a = temp1.dataset._model.call('fields_get').then(function(result) { fields = result });

*/
