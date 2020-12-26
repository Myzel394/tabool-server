from apps.django.utils.autocomplete_view import AutocompleteFieldView
from ....models import Homework

__all__ = [
    "HomeworkAutocompleteView"
]


class HomeworkAutocompleteView(AutocompleteFieldView):
    model = Homework
    field = "type"
