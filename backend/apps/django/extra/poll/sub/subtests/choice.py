from django.test import TestCase

from apps.django.extra.poll.models.choice import random_color


class ChoiceTest(TestCase):
    def test_random_color(self):
        color = random_color()
