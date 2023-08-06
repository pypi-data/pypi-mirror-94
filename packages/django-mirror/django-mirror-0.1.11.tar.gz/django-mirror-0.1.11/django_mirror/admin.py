from django_mirror.widgets import AdminMirrorArea


class MirrorAdmin:
    """
    Mixin for ModelAdmin subclasses which provides the mirror_fields option,
    used for listing fields to be rendered with the MirrorArea widget.

    mirror_fields can be either a list of field names, or a list of tuples
    where the first item is the field name and the second item is a dict of
    options to be passed to the widget.

    This mixin just provides another way to use the MirrorArea widget in the
    admin; this could be also done by subclassing the model form or by using
    the formfield_overrides option.
    """
    mirror_fields = tuple()

    def get_mirror_fields(self, request, obj=None):
        """
        Hook for specifying custom mirror fields.
        """
        return self.mirror_fields

    def _update_form_factory_kwargs(self, request, obj=None, **kwargs):
        """
        Update kwargs['widgets'] to include the mirror area widgets as defined
        in the mirror_fields option.

        Helper for the get_form and get_formset methods.
        """
        mirror_fields = self.get_mirror_fields(request, obj)
        mirror_widgets = {}

        for field in mirror_fields:
            if isinstance(field, (list, tuple)):
                field_name = field[0]
                widget_args = field[1]
            else:
                field_name = str(field)
                widget_args = {}

            mirror_widgets[field_name] = AdminMirrorArea(**widget_args)

        if mirror_widgets:
            if 'widgets' in kwargs and kwargs['widgets'] is not None:
                kwargs['widgets'].update(mirror_widgets)
            else:
                kwargs['widgets'] = mirror_widgets

        return kwargs

    def get_form(self, request, obj=None, **kwargs):
        """
        Overwrite ModelAdmin's get_form method in order to update the widgets
        argument for the modelform_factory.
        """
        kwargs = self._update_form_factory_kwargs(request, obj, **kwargs)
        return super().get_form(request, obj, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        """
        Overwrite InlineModelAdmin's get_formset method in order to update the
        widgets argument for the inlineformset_factory.
        """
        kwargs = self._update_form_factory_kwargs(request, obj, **kwargs)
        return super().get_formset(request, obj, **kwargs)
