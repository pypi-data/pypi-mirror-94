/**
 * Display a list item for a config page.
 *
 * The list item will show information on the item and any actions that can
 * be invoked.
 *
 * By default, this will show the text from the ListItem model, linking it
 * if the model has an editURL attribute. This can be customized by subclasses
 * by overriding `template`.
 */
Djblets.Config.ListItemView = Backbone.View.extend({
    tagName: 'li',
    className: 'config-forms-list-item',
    iconBaseClassName: 'djblets-icon',

    actionHandlers: {},

    template: _.template(dedent`
        <% if (editURL) { %>
        <a href="<%- editURL %>"><%- text %></a>
        <% } else { %>
        <%- text %>
        <% } %>
    `),

    /**
     * Initialize the view.
     */
    initialize() {
        this.listenTo(this.model, 'actionsChanged', this.render);
        this.listenTo(this.model, 'request', this.showSpinner);
        this.listenTo(this.model, 'sync', this.hideSpinner);
        this.listenTo(this.model, 'destroy', this.remove);

        this.$spinnerParent = null;
        this.$spinner = null;
    },

    /**
     *  Render the view.
     *
     * This will be called every time the list of actions change for
     * the item.
     *
     * Returns:
     *     Djblets.Config.ListItemView:
     *     This view.
     */
    render() {
        this.$el
            .empty()
            .append(this.template(_.defaults(
                this.model.attributes,
                this.getRenderContext()
            )));
        this.addActions(this.getActionsParent());

        return this;
    },

    /**
     * Return additional render context.
     *
     * By default this returns an empty object. Subclasses can use this to
     * provide additional values to :js:attr:`template` when it is rendered.
     *
     * Returns:
     *     object:
     *     Additional rendering context for the template.
     */
    getRenderContext() {
        return {};
    },

    /**
     * Remove the item.
     *
     * This will fade out the item, and then remove it from view.
     */
    remove() {
        this.$el.fadeOut('normal',
                         () => Backbone.View.prototype.remove.call(this));
    },

    /**
     * Return the container for the actions.
     *
     * This defaults to being this element, but it can be overridden to
     * return a more specific element.
     *
     * Returns:
     *     jQuery:
     *     The container for the actions.
     */
    getActionsParent() {
        return this.$el;
    },

    /**
     * Display a spinner on the item.
     *
     * This can be used to show that the item is being loaded from the
     * server.
     */
    showSpinner() {
        if (this.$spinner) {
            return;
        }

        this.$spinner = $('<span>')
            .addClass('fa fa-spinner fa-pulse config-forms-list-item-spinner')
            .prependTo(this.$spinnerParent)
            .hide()
            .css('visibility', 'visible')
            .fadeIn();
    },

    /**
     * Hide the currently visible spinner.
     */
    hideSpinner() {
        if (!this.$spinner) {
            return;
        }

        /*
         * The slow fadeout does two things:
         *
         * 1) It prevents the spinner from disappearing too quickly
         *    (in combination with the fadeIn above), in case the operation
         *    is really fast, giving some feedback that something actually
         *    happened.
         *
         * 2) By fading out, it doesn't look like it just simply stops.
         *    Helps provide a sense of completion.
         */
        this.$spinner.fadeOut('slow', () => {
            this.$spinner.remove();
            this.$spinner = null;
        });
    },

    /**
     * Add all registered actions to the view.
     *
     * Args:
     *     $parentEl (jQuery):
     *         The parent element to add the actions to.
     */
    addActions($parentEl) {
        const $actions = $('<span>')
            .addClass('config-forms-list-item-actions');

        this.model.actions.forEach(action => {
            const $action = this._buildActionEl(action)
                .appendTo($actions);

            if (action.children) {
                if (action.label) {
                    $action.append(' &#9662;');
                }

                /*
                 * Show the dropdown after we let this event propagate.
                 */
                $action.click(() => _.defer(
                    () => this._showActionDropdown(action, $action)
                ));
            }
        });

        this.$spinnerParent = $actions;

        $actions.prependTo($parentEl);
    },

    /**
     * Show a dropdown for a menu action.
     *
     * Args:
     *     action (object):
     *         The action to show the dropdown for. See
     *         :js:class:`Djblets.Config.ListItem`. for a list of attributes.
     *
     *     $action (jQuery):
     *         The element that represents the action.
     */
    _showActionDropdown(action, $action) {
        const actionPos = $action.position();
        const $pane = $('<ul/>')
                .css('position', 'absolute')
                .addClass('action-menu')
                .click(e => e.stopPropagation());
        const actionLeft = actionPos.left + $action.getExtents('m', 'l');

        action.children.forEach(
            childAction => $('<li/>')
                .addClass(`config-forms-list-action-row-${childAction.id}`)
                .append(this._buildActionEl(childAction))
                .appendTo($pane)
        );

        this.trigger('actionMenuPopUp', {
            action: action,
            $action: $action,
            $menu: $pane
        });

        $pane.appendTo($action.parent());

        const winWidth = $(window).width();
        const paneWidth = $pane.width();

        $pane.move(($action.offset().left + paneWidth > winWidth
                    ? actionLeft + $action.innerWidth() - paneWidth
                    : actionLeft),
                   actionPos.top + $action.outerHeight(),
                   'absolute');

        /* Any click outside this dropdown should close it. */
        $(document).one('click', () => {
            this.trigger('actionMenuPopDown', {
                action: action,
                $action: $action,
                $menu: $pane
            });

            $pane.remove();
        });
    },

    /**
     * Build the element for an action.
     *
     * If the action's type is ``'checkbox'``, a checkbox will be shown.
     * Otherwise, the action will be shown as a button.
     *
     * Args:
     *     action (object):
     *         The action to show the dropdown for. See
     *         :js:class:`Djblets.Config.ListItem`. for a list of attributes.
     */
    _buildActionEl(action) {
        const actionHandlerName = (action.enabled !== false
                                   ? this.actionHandlers[action.id]
                                   : null);
        const isCheckbox = (action.type === 'checkbox');
        const isRadio = (action.type === 'radio');

        let $action;
        let $result;

        if (isCheckbox || isRadio) {
            const inputID = _.uniqueId('action_' + action.type);
            $action = $('<input/>')
                .attr({
                    name: action.name,
                    type: action.type,
                    id: inputID
                });
            const $label = $('<label>')
                .attr('for', inputID)
                .text(action.label);

            if (action.id) {
                $label.addClass(`config-forms-list-action-label-${action.id}`);
            }

            $result = $('<span/>')
                .append($action)
                .append($label);

            if (action.propName) {
                if (isCheckbox) {
                    $action.bindProperty('checked', this.model,
                                         action.propName);
                } else if (isRadio) {
                    $action.bindProperty(
                        'checked', this.model, action.propName, {
                            radioValue: action.radioValue
                        }
                    );
                }
            }

            if (action.enabledPropName) {
                $action.bindProperty(
                    'disabled', this.model, action.enabledPropName,
                    {
                        inverse: (action.enabledPropInverse !== true)
                    });
            }

            if (actionHandlerName) {
                const actionHandler = _.debounce(
                    _.bind(this[actionHandlerName], this),
                    50,
                    true
                );

                $action.change(actionHandler);

                if (isRadio && action.dispatchOnClick) {
                    $action.click(actionHandler);
                }
            }
        } else {
            $action = $result = $('<a class="btn">')
                .text(action.label || '');

            if (action.iconName) {
                $action.append($('<span>')
                    .addClass(this.iconBaseClassName)
                    .addClass(`${this.iconBaseClassName}-${action.iconName}`));
            }

            if (actionHandlerName) {
                $action.click(_.bind(this[actionHandlerName], this));
            }
        }

        if (action.id) {
            $action.addClass(`config-forms-list-action-${action.id}`);
        }

        if (action.danger) {
            $action.addClass('danger');
        }

        if (action.enabled === false) {
            $action.prop('disabled', true);
            $result.addClass('disabled');
        }

        return $result;
    },
});
