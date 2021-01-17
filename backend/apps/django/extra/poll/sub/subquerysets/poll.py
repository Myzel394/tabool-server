from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

__all__ = [
    "PollQuerySet"
]


class PollQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user) -> "PollQuerySet":
        return self.filter(targeted_user__in=[user]).distinct()
