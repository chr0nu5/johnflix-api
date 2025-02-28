import uuid

from django.conf import settings
from django.core.cache import cache
from django.db.models import F
from rest_framework.response import Response


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


class HashFilterMixin(object):
    def filter_hash(self, queryset):
        hash_param = self.request.query_params.get("hash")
        if hash_param is not None:
            return queryset.filter(hash=hash_param)
        return queryset


class OrderingMixin(object):
    allowed_order_fields = {}

    def filter_ordering(self, queryset):
        order_by = self.request.query_params.get("order_by", "created_date")
        order_direction = self.request.query_params.get(
            "order_direction", "asc").lower()

        if order_by and (order_by in self.allowed_order_fields):
            model_field = self.allowed_order_fields[order_by]

            # Use NullsLast or NullsFirst to handle None values
            if order_direction == "desc":
                ordering_field = F(model_field).desc(nulls_last=True)
            else:
                ordering_field = F(model_field).asc(nulls_first=True)

            return queryset.order_by(ordering_field)

        return queryset


class CachedListMixin(object):
    def get_cache_key(self):
        user = self.request.user
        query_params = self.request.GET.dict()
        sorted_params = sorted(query_params.items())
        query_string = "&".join(["{}={}".format(k, v)
                                 for k, v in sorted_params])
        user_flag = "super" if user.is_superuser else "normal"

        return str(uuid.uuid1())

        key = "cache:{}:{}:{}".format(
            self.request.get_full_path(), user_flag, query_string)
        return key

    def list(self, request, *args, **kwargs):
        key = self.get_cache_key()
        cached_data = cache.get(key)
        if cached_data is not None:
            return Response(cached_data)
        response = super(CachedListMixin, self).list(request, *args, **kwargs)
        cache.set(key, response.data, settings.CACHE_TTL)
        return response
