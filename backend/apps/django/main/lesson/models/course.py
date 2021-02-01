from typing import *

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import LifecycleModel

from apps.django.main.authentication.models import Student
from apps.django.main.homework.models import Homework
from apps.django.main.school_data.public import *
from apps.django.main.school_data.public import model_names as school_names
from .lesson import Lesson
from ..public import model_names
from ..querysets import CourseQuerySet

if TYPE_CHECKING:
    from django.contrib.auth import get_user_model
    from apps.django.main.school_data.models import Subject, Teacher

__all__ = [
    "Course"
]


class Course(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.COURSE
        verbose_name_plural = model_names.COURSE_PLURAL
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
        verbose_name=school_names.SUBJECT
    )  # type: Subject
    
    teacher = models.ForeignKey(
        TEACHER,
        on_delete=models.SET_NULL,
        verbose_name=school_names.TEACHER,
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
        try:
            class_number = self.get_class_number()
        except TypeError:
            prefix = "unknown_class_number"
        else:
            prefix = str(class_number)
        
        return f"{prefix}/{self.name}/{self.id}"
    
    def get_class_number(self) -> int:
        # Get a class number from a student
        for participant in self.participants.all():
            if student := getattr(participant, "student", None):  # type: Student
                return student.class_number
        
        raise TypeError("Course has no participants. Class number can't be detected.")
