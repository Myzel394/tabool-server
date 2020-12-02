from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination as DRFPNPagination
from rest_framework.response import Response

__all__ = [
    "PageNumberPagination"
]


class PageNumberPagination(DRFPNPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.page.next_page_number() if self.page.has_next() else None),
            ('previous', self.page.previous_page_number() if self.page.has_previous() else None),
            ('results', data)
        ]))
