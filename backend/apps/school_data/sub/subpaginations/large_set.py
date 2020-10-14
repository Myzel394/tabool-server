from rest_framework.pagination import PageNumberPagination

__all__ = [
    "LargeSetPagination"
]


class LargeSetPagination(PageNumberPagination):
    page_size = 100
