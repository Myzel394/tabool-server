from django.db import models

from apps.django.utils.models import ScoosoDataMixin
from ...public import *
from ...public import model_names

__all__ = [
    "SubmissionScoosoData"
]


class SubmissionScoosoData(ScoosoDataMixin):
    class Meta:
        verbose_name = model_names.SUBMISSION_SCOOSO
        verbose_name_plural = model_names.SUBMISSION_SCOOSO_PLURAL
        ordering = ("submission", "scooso_id")
    
    submission = models.OneToOneField(
        SUBMISSION,
        on_delete=models.CASCADE,
        verbose_name=model_names.SUBMISSION
    )
    
    def __str__(self):
        return str(self.submission)
