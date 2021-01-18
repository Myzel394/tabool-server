from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

__all__ = [
    "PollQuerySet"
]


class PollQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user) -> "PollQuerySet":
        return self.filter(targeted_user__in=[user]).distinct()
    
    def voted(self, user) -> "PollQuerySet":
        return self.filter(vote__associated_user=user)
    
    def not_voted(self, user) -> "PollQuerySet":
        return self.exclude(vote__associated_user=user)
