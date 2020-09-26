from rest_framework.pagination import PageNumberPagination

__all__ = [
    "TimetableLessonPagination"
]


class TimetableLessonPagination(PageNumberPagination):
    page_size = 50
