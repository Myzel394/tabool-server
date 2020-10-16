from rest_framework.pagination import PageNumberPagination

__all__ = [
    "LessonPagination"
]


class LessonPagination(PageNumberPagination):
    page_size = 200
