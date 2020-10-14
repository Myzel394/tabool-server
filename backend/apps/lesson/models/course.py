from typing import *

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_hint import *
from django_lifecycle import AFTER_SAVE, hook, LifecycleModel

import apps.school_data.public.model_references
import apps.school_data.public.model_verbose_functions
from apps.homework.models import Homework
from .lesson import Lesson
from ..querysets import CourseQuerySet

if TYPE_CHECKING:
    from django.contrib.auth import get_user_model
    from apps.school_data.models import Subject, Teacher

__all__ = [
    "Course"
]


class Course(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Kurs")
        verbose_name_plural = _("Kurse")
    
    RELATION_MODELS = {Lesson, Homework}
    
    objects = CourseQuerySet.as_manager()
    
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Teilnehmer"),
    )  # type: get_user_model()
    
    subject = models.ForeignKey(
        apps.school_data.public.model_references.SUBJECT,
        verbose_name=apps.school_data.public.model_verbose_functions.subject_single,
        on_delete=models.CASCADE,
    )  # type: Subject
    
    teacher = models.ForeignKey(
        apps.school_data.public.model_references.TEACHER,
        verbose_name=apps.school_data.public.model_verbose_functions.teacher_single,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )  # type: Teacher
    
    course_number = models.PositiveSmallIntegerField(
        verbose_name=_("Kursnummer"),
        default=1
    )  # type: int
    
    def __call_manage_relations_on_model(self, models: Iterable[StandardModelType]) -> None:
        participants = self.participants.all()
        participants_list = list(participants)
        
        for model in models:
            model.objects.manage_relations(participants_list, self)
    
    @hook(AFTER_SAVE)
    def _call_manage_relations_on_related_models(self) -> None:
        self.__call_manage_relations_on_model(self.RELATION_MODELS)
    
    def update_relations(self, targeted_models: Optional[Set[StandardModelType]] = None) -> None:
        if targeted_models:
            assert all([
                x in self.RELATION_MODELS
                for x in targeted_models
            ]), "Not all models were found in `self.RELATION_MODELS`. Maybe you forgot adding it?"
        else:
            targeted_models = self.RELATION_MODELS
        
        self.__call_manage_relations_on_model(targeted_models)
    
    @property
    def name(self) -> str:
        return f"{self.subject.name}{self.course_number}".lower()
