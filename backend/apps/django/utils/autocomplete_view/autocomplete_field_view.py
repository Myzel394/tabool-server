from abc import ABC

from django.db.models import F

from apps.django.utils.autocomplete_view.autocomplete_view import AutocompleteView, T
from apps.django.utils.autocomplete_view.type_hints import DefaultResultType


class AutocompleteFieldView(AutocompleteView, ABC):
    field: str
    max_results: int = 20
    
    def get_qs(self, user: "User") -> T:
        return self.model.objects.from_user(user)
    
    def filter_qs(self, qs: T, query: str) -> T:
        return qs.only(self.field).filter(**{
            f"{self.field}__trigram_similar": query
        })
    
    def serialize_qs(self, qs: T) -> list[DefaultResultType]:
        return qs.annotate(text=F(self.field)).values("id", "text").distinct()[:self.max_results]
