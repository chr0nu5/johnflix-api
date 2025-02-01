class HiddenFilterMixin(object):
    def filter_hidden(self, queryset):
        if not self.request.user.is_superuser:
            return queryset.filter(hidden=False)
        hidden_param = self.request.query_params.get("hidden")
        if hidden_param is not None:
            if hidden_param.lower() == "true":
                return queryset.filter(hidden=True)
            elif hidden_param.lower() == "false":
                return queryset.filter(hidden=False)
        return queryset


class OrderingMixin(object):
    allowed_order_fields = {}

    def filter_ordering(self, queryset):
        order_by = self.request.query_params.get("order_by")
        order_direction = self.request.query_params.get(
            "order_direction", "asc").lower()
        if order_by and (order_by in self.allowed_order_fields):
            model_field = self.allowed_order_fields[order_by]
            if order_direction == "desc":
                ordering_field = "-{}".format(model_field)
            else:
                ordering_field = model_field
            return queryset.order_by(ordering_field)
        return queryset
