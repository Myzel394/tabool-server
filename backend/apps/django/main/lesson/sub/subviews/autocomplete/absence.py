from apps.django.utils.autocomplete_view import AutocompleteFieldView
from ....models import LessonAbsence

__all__ = [
    "AbsenceReasonAutocompleteView"
]


class AbsenceReasonAutocompleteView(AutocompleteFieldView):
    model = LessonAbsence
    field = "reason"
