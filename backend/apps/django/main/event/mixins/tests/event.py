from abc import ABC

import lorem

from apps.django.main.school_data.mixins.tests import *
from apps.django.utils.tests_mixins import *
from ...models import Event


class EventTestMixin(RoomTestMixin, StartTimeEndTimeTestMixin, DateUtilsTestMixin, ABC):
    DURATION = 60 * 3
    
    @classmethod
    def Create_event(cls, **kwargs) -> Event:
        return Event.objects.create(
            **joinkwargs(
                {
                    "room": cls.Create_room,
                    "title": lorem.sentence,
                    "start_datetime": cls.Random_allowed_datetime,
                    "end_datetime": cls.Random_allowed_datetime,
                },
                kwargs
            )
        )
