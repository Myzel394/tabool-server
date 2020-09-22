from abc import ABC

import lorem

from apps.subject.mixins.tests import RoomTestMixin
from apps.utils.tests import StartTimeEndTimeTestMixin
from ...models import Event


class EventTestMixin(RoomTestMixin, StartTimeEndTimeTestMixin, ABC):
    DURATION = 60 * 3
    
    @classmethod
    def Create_event(cls, **kwargs) -> Event:
        return Event.objects.create(
            **{
                "room": cls.Create_room(),
                "title": lorem.sentence(1),
                "start_datetime": cls.start_time(),
                "end_datetime": cls.end_time(),
                **kwargs
            }
        )
