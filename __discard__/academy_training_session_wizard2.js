odoo.define("academy_base.widgets", function (require) {

    "use strict";

    var core = require("web.core");
    var form_common = require("web.form_common");
    var form_relational = require('web.form_relational');
    var Model = require("web.DataModel");
    var ViewManager = require('web.ViewManager');
    var data = require('web.data');
    var ListView = require('web.ListView');
    var data_manager = require('web.data_manager');

    var QWeb = core.qweb;



    var AcademyTrainingActionUnitControlSelector = form_relational.AbstractManyField.extend({

        template: 'FieldMany2ManyClick',
        model: false,
        loading: false,
        starting: false,
        tree_view: false,
        fullset: false,
        view_obj: false,
        fields: [],
        extra_rows: [],


        init: function(field_manager, node) {
            this._super(field_manager, node);

            var deferred = jQuery.Deferred();

            console.log(this);
            //this.__edispatcherRegisteredEvents = []; // remove all bind events

            self.loading = deferred.promise();
            self._get_model();

            self._get_default_tree_view().done(function() {
                self._get_fields().done(function() {
                    deferred.resolve();
                });
            });

            self._initialize_fullset();

            return result;
        },

        willStart: function () {
            var self = this;
            var result = self._super.apply(self, arguments);

            var deferred = jQuery.Deferred();
            self.starting = deferred.promise();

            self.loading.done(function() {
                self._reload_fullset().done(function() {
                    self._fetch_fullset().done(function() {
                        deferred.resolve();
                    });
                });
            });

            return result;
        },

        destroy: function() {
            var self = this;
            var result = self._super.apply(self, arguments);

            self._destroy_fullset();

            return result;
        },


        /**
         * Gets the related model name
         --------------------------------------------------------------------*/
        _get_model: function() {
            var self = this;
            self.model = self.dataset.model;
        },


        /**
         * Gets all fields in default tree view, if tree_view attribute has not
         * be set, this calls _get_default_tree_view before.
         --------------------------------------------------------------------*/
        _get_fields: function() {
            var self = this;

            var deferred = jQuery.Deferred();

            jQuery.each(self.tree_view.fields, function(key, item) {
                self.fields.push(key);
                deferred.resolve(self.fields);
            });

            return deferred.promise();
        },


        /*
         * Gets default tree view for model
         --------------------------------------------------------------------*/
        _get_default_tree_view: function() {
            var self = this;
            var deferred = jQuery.Deferred();

            self.dataset.call('fields_view_get', {view_type: 'tree'})
                .then(function(result) {
                    self.tree_view = result;
                    deferred.resolve(result);
                }
            );

            return deferred.promise();
        },


        /*
         * Creates new set to read and store all potential values
         --------------------------------------------------------------------*/
        _initialize_fullset: function () {
            var self = this;

            self._destroy_fullset();

            self.fullset = new data.DataSet(
                this,
                "academy.training.action.unit.control",
                self.context
            );
        },


        /*
         * Loads all ids for recordet
         --------------------------------------------------------------------*/
        _reload_fullset: function () {
            var self = this;
            var deferred = new jQuery.Deferred();

            self.fullset.call('search', {args: []})
                .then(function(ids) {
                    self.fullset.ids = ids;
                    deferred.resolve(ids);
                 });

            return deferred.promise();
        },

        /*
         * Destroys created (auxiliary) recordset
         --------------------------------------------------------------------*/
        _destroy_fullset: function() {
            if (self.fullset !== false) {
                delete self.fullset;
                self.fullset = false;
            }
        },

        renderElement: function(no_recurse) {
            var self = this;
            // var result =  self._super.apply(self, arguments);

            console.log('renderElement');

            // self.$el.find("tbody tr").on("click", {widget: self}, self._on_row_click);

            var deferred = jQuery.Deferred();

            self.starting.done(function(){
                self.fullset.read_ids(self.fullset.ids, this.fields)
                    .then(function(data) {
                        deferred.resolve(data);
                });

               deferred.done(function(data) {

                    self.extra_rows = _.range(Math.max(0, 5 - data.length));
                    console.log(self.fullset.data);
                    self.$el.html(QWeb.render(self.template, {widget: self}));
                });
            });

        },

        _fetch_value: function(){
            var self = this;
            var deferred = jQuery.Deferred();

            self.dataset.read_ids(self.get('value'), self.fields)
            .then(function(data) {
                deferred.resolve(data);
            });

            return deferred.promise();
        },

        _fetch_fullset: function() {
            var self = this;
            var deferred = jQuery.Deferred();
            var fields_to_read = _.union(self.fields, ['id']);

            self.fullset.cache = {};
            self.fullset.read_ids(self.fullset.ids, fields_to_read)
                .then(function(records) {
                    /* HACK - whould be another way */
                    self.fullset.data = [];
                    deferred.resolve(records);
                });

            return deferred.promise();
        },



    }); /*-- AcademyTrainingActionUnitControlSelector -- */



    core.form_widget_registry.add("x2manyselector", AcademyTrainingActionUnitControlSelector);

    return AcademyTrainingActionUnitControlSelector;

}); /*-- odoo.define -- */


/* todo

    - [ ] destroy
    - [ ] ensure id is readed on _fech_fullset

*/
