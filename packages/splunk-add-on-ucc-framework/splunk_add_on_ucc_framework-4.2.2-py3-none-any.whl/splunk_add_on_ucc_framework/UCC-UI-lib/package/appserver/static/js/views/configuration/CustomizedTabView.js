import Backbone from 'backbone';
import {generateModel} from 'app/util/backboneHelpers';
import {generateValidators} from 'app/util/modelValidators';
import {generateCollection} from 'app/util/backboneHelpers';
import NormalTabView from './NormalTabView';
import TableBasedTabView from './TableBasedTabView';
import restEndpointMap from 'app/constants/restEndpointMap';

export default Backbone.View.extend({
    initialize: function(options) {
        this.initOptions = options;

        this.isTableBasedView = !!options.props.table;
        this.props = options.props;

        // This id will be used by QA team for testes
        this.submitBtnId = `add${this.props.title.replace(/ /g, '')}Btn`;

        this.initDataBinding();
    },

    initDataBinding: function() {
        const {name} = this.props;
        const preDefinedUrl = restEndpointMap[name];

        if (this.isTableBasedView) {
            this.dataStore = generateCollection(preDefinedUrl ? '' : name, {
                endpointUrl: preDefinedUrl
            });
        } else {
            const {entity, options} = this.props,
                validators = generateValidators(entity),
                formValidator = options ? options.saveValidator : undefined;

            this.dataStore = new (generateModel(
                    preDefinedUrl ? undefined : 'settings',
                    {
                        modelName: name,
                        fields: entity,
                        endpointUrl: preDefinedUrl,
                        formDataValidatorRawStr: formValidator,
                        onLoadRawStr: options ? options.onLoad : undefined,
                        shouldInvokeOnload: true,
                        validators
                    }
                )
            )({name});
            this.dataStore.attr_labels = {};
            entity.forEach(({field, label}) => {
                this.dataStore.attr_labels[field] = label;
            });
        }
    },

    render: function() {
        const {dataStore, submitBtnId} = this;
        let view;
        if (this.isTableBasedView) {
            view = new TableBasedTabView(
                {...this.initOptions, dataStore, submitBtnId}
            );
        } else {
            view = new NormalTabView(
                {...this.initOptions, dataStore, submitBtnId}
            );
        }
        this.$el.html(view.render().$el);

        return this;
    }
});
