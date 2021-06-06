from abc import ABC

from django.db.models import Count, F

from apps.django.utils.autocomplete_view.autocomplete_view import AutocompleteView, T
from apps.django.utils.autocomplete_view.type_hints import DefaultResultType


class AutocompleteFieldView(AutocompleteView, ABC):
    field: str
    max_results: int = 20
    return_all_when_empty: bool = True

    def get_qs(self, user: "User") -> T:
        return self.model.objects.from_user(user)

    def filter_qs(self, qs: T, query: str) -> T:
        if query == "" and self.return_all_when_empty:
            return qs

        filters = {
            f"{self.field}__trigram_similar": query
        }

        return qs \
            .only(self.field) \
            .filter(**filters)

    def serialize_qs(self, qs: T) -> list[DefaultResultType]:
        count = qs \
            .values(self.field) \
            .annotate(count=Count(self.field)) \
            .order_by(f"-{self.field}")

        return count \
                   .annotate(text=F(self.field)) \
                   .values("text", "count") \
                   .filter(count__gt=0) \
                   .distinct()[:self.max_results]
