from abc import ABC

import lorem

from apps.lesson.mixins.tests import RoomTestMixin
from apps.utils.tests import DateUtilsTestMixin, joinkwargs, StartTimeEndTimeTestMixin
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
