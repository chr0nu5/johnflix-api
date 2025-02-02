from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'limit': self.get_page_size(self.request),
            'current_count': len(data),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
