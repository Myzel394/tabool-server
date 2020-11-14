from abc import ABC

import lorem

from apps.django.main.lesson.mixins.tests import CourseTestMixin
from apps.django.main.school_data.mixins.tests import *
from apps.django.utils.tests import *
from ...models import Event, Modification


class ModificationTestMixin(RoomTestMixin, StartTimeEndTimeTestMixin, DateUtilsTestMixin, CourseTestMixin, ABC):
    DURATION = 60 * 3
    
    @classmethod
    def Create_modification(cls, **kwargs) -> Event:
        return Modification.objects.create(
            **joinkwargs(
                {
                    "course": cls.Create_course,
                    "new_room": cls.Create_room,
                    "new_subject": cls.Create_subject,
                    "new_teacher": cls.Create_teacher,
                    "start_datetime": cls.Random_allowed_datetime,
                    "end_datetime": cls.Random_allowed_datetime,
                    "information": lorem.paragraph,
                },
                kwargs
            )
        )
