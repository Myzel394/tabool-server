import json
import random
from pathlib import Path

from django.test import TestCase

from apps.lesson.mixins.tests import RoomTestMixin
from apps.lesson.sub.subserializers import RoomScoosoDataSerializer


class SerializerCreationTest(RoomTestMixin):
    def setUp(self) -> None:
        for _ in range(5):
            self.Create_room()
        
        self.room = self.Create_room()
        self.data = json.load(Path("scooso_data.json"))
        schedules = self.data["tables"]["schedule"]
        self.random_lesson = random.choice(schedules)
    
    def test_serializer(self):
        serializer = RoomScoosoDataSerializer(self.room).data
    
    def test_reverse_serializer(self):
        room = self.Create_room()
        room.delete()
        
        data = RoomScoosoDataSerializer(room).data
        serializer = RoomScoosoDataSerializer(data=data)
        serializer.is_valid(True)
        new_room = serializer.save()

