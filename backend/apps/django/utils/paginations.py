from collections import OrderedDict

from django.conf import settings
from rest_framework.pagination import PageNumberPagination as DRFPNPagination
from rest_framework.response import Response

__all__ = [
    "PageNumberPagination"
]


class PageNumberPagination(DRFPNPagination):
    page_size_query_param = "page_size"
    max_page_size = settings.REST_MAX_PAGE_SIZE

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.page.next_page_number() if self.page.has_next() else None),
            ('previous', self.page.previous_page_number() if self.page.has_previous() else None),
            ('results', data)
        ]))
