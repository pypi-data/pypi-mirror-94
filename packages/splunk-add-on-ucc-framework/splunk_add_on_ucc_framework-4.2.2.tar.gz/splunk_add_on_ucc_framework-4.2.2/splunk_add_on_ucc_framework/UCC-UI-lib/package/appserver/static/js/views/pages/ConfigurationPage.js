import {configManager} from 'app/util/configManager';
import CustomizedTabView from 'app/views/configuration/CustomizedTabView';
import 'appCssDir/common.css';
import 'appCssDir/configuration.css';

define([
    'jquery',
    'lodash',
    'backbone',
    'app/templates/common/PageTitle.html',
    'app/templates/common/TabTemplate.html'
], function (
    $,
    _,
    Backbone,
    PageTitleTemplate,
    TabTemplate
) {
    return Backbone.View.extend({
        initialize: function() {
            const {unifiedConfig: {pages: {configuration}}} = configManager;
            this.stateModel = new Backbone.Model({
                selectedTabId: this._generateTabId(configuration.tabs)
            });

            this.tabNameUsed = false;
        },

        events: {
            "click ul.nav-tabs > li > a": function (e) {
                e.preventDefault();
                const tabId = e.currentTarget.id.slice(0, -3);
                this.changeTab(tabId);
            }
        },

        render: function () {
            const { unifiedConfig: { pages: { configuration } } } = configManager;

            const header = this._parseHeader(configuration);
            this.$el.append(_.template(PageTitleTemplate)(header));
            this.$el.append(_.template(TabTemplate));

            const tabs = this._parseTabs(configuration);
            this.renderTabs(tabs);
            return this;
        },

        changeTab: function (tabId) {

            if (tabId === null) return;
            const { unifiedConfig: { pages: { configuration } } } = configManager;
            let queryParams = new URLSearchParams(location.search);
            let tabName = queryParams.get('tab');
            // For the first time, this.tabNameUsed will be false.
            // From the next time onwards, it will be true. So condition will be false.
            // So when the tab is changed by the user, this condition will be false and else part will be executed
            if(tabName && configuration.tabs.length>0 && !this.tabNameUsed) {
                for (var i = 0; i < configuration.tabs.length; i++) {
                    if (configuration.tabs[i].title.toLowerCase().replace(/ /g, '-') === tabName) {
                        this.tabNameUsed = true;
                        this._activateTab(tabId);
                        break;
                    }
                }
                // If no tab is matched with the tab name provided, activate first tab by default
                if (!this.tabNameUsed) {
                    this.tabNameUsed = true;
                    this._activateTab(configuration.tabs[0].title.toLowerCase().replace(/ /g, '-'));
                }
            } else {
                this._activateTab(tabId);
            }
        },

        /**
         * Method to activate the tab based on params value or URL Query Parameters e.g. ..../pageName?tab=mytab
         * If tab name is incorrect, it will open the first tab by default.
         * @param params = Tab Name
         */
        _activateTab(tabId){
            this.tabName = tabId;
            $('.nav-tabs li').removeClass('active');
            $('#' + this.tabName + '-li').parent().addClass('active');
            $('.tab-content div').removeClass('active');
            $(`#${tabId}-tab`).addClass('active');
            this.stateModel.set('selectedTabId', `#${tabId}-tab`);
        },

        _parseHeader({title, description}) {
            return {
                title: title ? title : '',
                description: description ? description : '',
                enableButton: false,
                enableHr: false
            };
        },

        _generateTabToken(tabs, title) {
            return (title || tabs[0].title).toLowerCase().replace(/\s/g, '-');
        },

        _generateTabId(tabs, title) {
            if (!title) {
                title = tabs[0].title;
            }
            return `#${this._generateTabToken(tabs, title)}-tab`;
        },

        _parseTabs({tabs}) {
            return tabs.map((d, i) => {
                const {title} = d;
                const view = new CustomizedTabView({
                    containerId: this._generateTabId(tabs, title),
                    pageState: this.stateModel,
                    props: d
                });
                return {
                    active: i === 0,
                    title,
                    token: this._generateTabToken(tabs, title),
                    view
                };
            }).filter(d => !!d);
        },

        renderTabs: function (tabs) {
            _.each(tabs, tab => {
                const { title, token, view } = tab;
                let active;
                if (!this.tabName) {
                    active = tab.active ? 'active' : '';
                } else if (this.tabName && this.tabName === token) {
                    active = 'active';
                }
                this.$(".nav-tabs").append(
                    _.template(this.tabTitleTemplate)({title, token, active})
                );
                this.$(".tab-content").append(
                    _.template(this.tabContentTemplate)({token, active})
                );
                this.$(this._generateTabId(tabs, title)).html(
                    view.render().$el
                );
            });
        },

        tabTitleTemplate: `
            <li class="<%- active %>">
                <a href="#" id="<%- token %>-li">
                    <%- _(title).t() %>
                </a>
            </li>
        `,

        tabContentTemplate: `
            <div id="<%- token %>-tab" class="tab-pane <%- active %>">
            </div>
        `
    });
});
