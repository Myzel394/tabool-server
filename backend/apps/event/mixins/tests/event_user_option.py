from abc import ABC

from django.test import TestCase

from ...models import EventUserOption


class EventUserOptionTestMixin(TestCase, ABC):
    @classmethod
    def Create_event_user_option(cls, **kwargs) -> EventUserOption:
        return EventUserOption.objects.create(
            **{
                "event": cls.Create_event(),
                **kwargs
            }
        )
