from django.apps import apps
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

__all__ = [
    "SubjectQuerySet"
]


class SubjectQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user) -> "SubjectQuerySet":
        Course = apps.get_model(app_label="course", model_name="Course")
        
        subject_ids = Course.objects \
            .from_user(user) \
            .only("subject") \
            .values_list("subject", flat=True) \
            .distinct()
        
        return self.only("id").filter(id__in=subject_ids)
