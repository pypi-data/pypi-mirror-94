import _ from 'lodash';
import $ from 'jquery';
import Backbone from 'backbone';
import {configManager} from 'app/util/configManager';
import Util from 'app/util/Util';

export default Backbone.View.extend({
    initialize: function (options) {
        _.extend(this, options);
        // Global Config
        this.unifiedConfig = configManager.unifiedConfig;
        // State model
        this.stateModel = new Backbone.Model({
            sortKey: 'name',
            sortDirection: 'asc',
            count: 10,
            // Prevent triggering stateChange two times when search
            // Refer to FindInput.js
            offset: '0',
            fetching: true
        });
        // Event dispatcher
        this.dispatcher = _.extend({}, Backbone.Events);

        // Mapping from field to CustomCell
        this.fieldCustomCellMapping = new Map();

        // State model change event
        this.listenTo(
            this.stateModel,
            'change:search change:sortDirection change:sortKey ' +
            'change:offset change:count change:service',
            this.stateChange.bind(this)
        );

        // Delete model event
        this.listenTo(this.dispatcher, 'delete-input', (model) => {
            // Delete model from cache
            this.cachedCollection.models = this.cachedCollection.models.filter(
                m => {
                    return m.get('id') !== model.get('id');
                }
            );
            this.stateChange();
        });

        // Edit model event
        this.listenTo(this.dispatcher, 'edit-input', (model) => {
            // Update model in cache
            this.cachedCollection.models = this.cachedCollection.models.map(
                m => {
                    if (m.get('id') !== model.get('id')) {
                        return m;
                    } else {
                        return model;
                    }
                }
            );
            this.stateChange();
        });

        // Add input event
        this.listenTo(this.dispatcher, 'add-input', (model) => {
            if(!_.isUndefined(this.cachedCollection)) {
                this.cachedCollection.models.push(model);
                this.stateChange();
            }
        });
    },

    _getCompareText: function (model, attributeField, headerConfig) {
        const cellDef = _.find(
            headerConfig,
            (cell) => {
                return cell.field === attributeField;
            }
        );
        let fieldValue = null;
        if (model.entry.has(attributeField) || 
                model.entry.content.has(attributeField)) {
            fieldValue = model.entry.has(attributeField) ? 
                model.entry.get(attributeField) : 
                model.entry.content.get(attributeField);
        }

        if (cellDef && cellDef.mapping && fieldValue in cellDef.mapping) {
            return _.toString(cellDef.mapping[fieldValue]);
        } else if (cellDef && cellDef.customCell && cellDef.customCell.src) {
            const CustomCell = this.fieldCustomCellMapping.get(attributeField);
            const el = document.createElement('div');
            const service = Util.extractServiceName(model);
            const customCell = new CustomCell(
                this.unifiedConfig,
                service,
                el,
                attributeField,
                model
            );
            return customCell.render().el.innerText;
        } else {
            // Use model attribute value
            return _.toString(fieldValue);
        }
    },

    adjustPaging: function (collection, models) {
        const offset = Number(this.stateModel.get('offset')),
              count = this.stateModel.get('count'),
              total = models.length;
        collection.paging.set('offset', offset);
        collection.paging.set('perPage', count);
        collection.paging.set('total', total);
        _.each(models, (model) => {
            model.paging.set('offset', offset);
            model.paging.set('perPage', count);
            model.paging.set('total', total);
        });
        return models.slice(offset, offset + count);
    },

    fetchListCollection: function (collection) {
        this.stateModel.set('fetching', true);
        return collection.fetch({
            data: {
                count: 0 // fetch all stanzas
            },
            success: () => {
                this.stateModel.set('fetching', false);
            }
        });
    },

    getRawSearch: function(searchString) {
        if (searchString) {
            return searchString.substring(
                searchString.indexOf('*') + 1,
                searchString.indexOf('*', searchString.indexOf('*') + 1)
            ).toLowerCase();
        } else {
            return '';
        }
    },

    loadCustomCell: function (headerConfig) {
        return _.map(
            _.filter(
                headerConfig,
                h => h.customCell && h.customCell.src
            ),
            hr => this._loadCustomCell(hr.customCell.src, hr.field)
        );
    },

    _loadCustomCell: function(module, field) {
        const deferred = $.Deferred();
        __non_webpack_require__(['custom/' + module], (CustomCell) => {
            this.fieldCustomCellMapping.set(field, CustomCell);
            deferred.resolve(CustomCell);
        });
        return deferred.promise();
    }
});
