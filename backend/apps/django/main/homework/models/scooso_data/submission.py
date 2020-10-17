from django.db import models

from apps.django.utils.models import ScoosoDataMixin
from ...public import *
from ...public import model_verboses

__all__ = [
    "SubmissionScoosoData"
]


class SubmissionScoosoData(ScoosoDataMixin):
    class Meta:
        verbose_name = model_verboses.SUBMISSION_SCOOSO
        verbose_name_plural = model_verboses.SUBMISSION_SCOOSO_PLURAL
        ordering = ("submission", "scooso_id")
    
    submission = models.OneToOneField(
        SUBMISSION,
        on_delete=models.CASCADE,
        verbose_name=model_verboses.SUBMISSION
    )
    
    def __str__(self):
        return str(self.submission)
