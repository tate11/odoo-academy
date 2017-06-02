jQuery(document).ready(function() {

    odoo.define("academy_base.appointment_manager", function (require) {
        "use strict";
        var core = require('web.core');
        var web_widget = require('web.FormView')

        var FormWidgetOverride = web_widget.extend({

            on_form_changed: function() {
                this._super.apply(this, arguments);

                function hide_parent_row (event) {
                    jQuery('.o_form_field').parent('td').parent('tr').css('display', 'table-row');
                    jQuery('.o_row').parent('td').parent('tr').css('display', 'table-row');
                    jQuery('.o_form_invisible').parent('td').parent('tr').css('display', 'none');
                }

                jQuery('.o_form_invisible').parent('td').parent('tr').css('display', 'none');

                jQuery('.oe_field_allday').each(function () {
                    var oe_item = this;
                    jQuery(oe_item).change(hide_parent_row);
                }); /* each oe_field_allday */

                jQuery('.oe_field_rrule_type').each(function () {
                    var oe_item = this;
                    jQuery(oe_item).change(hide_parent_row);
                }); /* each oe_field_allday */

            }, /* on_form_changed */

        }); /* FormWidgetOverride */

        core.view_registry.add('form', FormWidgetOverride);

    }); /* odoo.define */

}); /* document.ready */
