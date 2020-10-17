from typing import *

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_hint import *
from django_lifecycle import LifecycleModel

from apps.django.main.authentication.models import Student
from apps.django.main.homework.models import Homework
from apps.django.main.school_data.public import *
from apps.django.main.school_data.public import model_verboses as school_verbose
from .lesson import Lesson
from ..public import model_verboses
from ..querysets import CourseQuerySet

if TYPE_CHECKING:
    from django.contrib.auth import get_user_model
    from apps.django.main.school_data.models import Subject, Teacher

__all__ = [
    "Course"
]


class Course(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = model_verboses.COURSE
        verbose_name_plural = model_verboses.COURSE_PLURAL
        ordering = ("subject", "teacher", "course_number")
    
    RELATION_MODELS = {Lesson, Homework}
    
    objects = CourseQuerySet.as_manager()
    
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Teilnehmer"),
    )  # type: get_user_model()
    
    subject = models.ForeignKey(
        SUBJECT,
        on_delete=models.CASCADE,
        verbose_name=school_verbose.SUBJECT
    )  # type: Subject
    
    teacher = models.ForeignKey(
        TEACHER,
        on_delete=models.SET_NULL,
        verbose_name=school_verbose.TEACHER,
        blank=True,
        null=True,
    )  # type: Teacher
    
    course_number = models.PositiveSmallIntegerField(
        verbose_name=_("Kursnummer"),
        default=1
    )  # type: int
    
    def __str__(self):
        return _("{course_name}: {teacher}").format(
            course_name=self.name,
            teacher=self.teacher or "-",
        )
    
    @property
    def name(self) -> str:
        return f"{self.subject.name}{self.course_number}".lower()
    
    @property
    def folder_name(self) -> str:
        if class_number := self.get_class_number():
            return f"{class_number}/{self.name}"
        return f"unknown/{self.name}"
    
    def get_class_number(self) -> Optional[int]:
        for participant in self.participants.all():
            if student := getattr(participant, "student", None):  # type: Student
                return student.class_number
        
        return None
