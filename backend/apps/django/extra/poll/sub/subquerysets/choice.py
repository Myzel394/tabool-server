from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

__all__ = [
    "ChoiceQuerySet"
]


class ChoiceQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user) -> "ChoiceQuerySet":
        return self.filter(poll__targeted_user__in=[user]).distinct()
