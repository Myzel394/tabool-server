from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_hint import QueryType
from django_lifecycle import LifecycleModel

from apps.django.authentication.user.models.user import User
from apps.django.authentication.user.public import *
from apps.django.authentication.user.public import model_names as auth_names
from ..public import *
from ..public import model_names
from ..querysets import CourseQuerySet

if TYPE_CHECKING:
    from apps.django.authentication.user.models import Teacher
    from . import Subject

__all__ = [
    "Course"
]


class Course(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.COURSE
        verbose_name_plural = model_names.COURSE_PLURAL
        ordering = ("subject", "teacher", "course_number")
    
    objects = CourseQuerySet.as_manager()
    
    participants = models.ManyToManyField(
        STUDENT,
        verbose_name=_("Teilnehmer"),
    )
    
    subject = models.ForeignKey(
        SUBJECT,
        on_delete=models.CASCADE,
        verbose_name=model_names.SUBJECT
    )  # type: Subject
    
    teacher = models.ForeignKey(
        TEACHER,
        on_delete=models.CASCADE,
        verbose_name=auth_names.TEACHER,
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
    
    @property
    def user_participants(self) -> QueryType[User]:
        user_ids = self.participants.all().values_list("user", flat=True).distinct()
        users = User.objects.only("id").filter(id__in=user_ids)
        
        return users
