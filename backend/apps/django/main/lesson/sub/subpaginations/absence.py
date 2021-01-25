from rest_framework.pagination import PageNumberPagination

__all__ = [
    "AbsencePagination"
]


class AbsencePagination(PageNumberPagination):
    page_size = 300
