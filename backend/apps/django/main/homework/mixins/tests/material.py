import random
import string
from datetime import datetime, timedelta

import lorem
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.django.main.homework.models import Material
from apps.django.main.timetable.mixins import joinkwargs, LessonTestMixin

__all__ = [
    "MaterialTestMixin"
]


class MaterialTestMixin(LessonTestMixin):
    @classmethod
    def Create_material(cls, **kwargs) -> Material:
        lesson = kwargs.pop("lesson", None) or cls.Create_lesson()
        random_id = "".join(random.choices(string.ascii_letters + string.digits, k=5))
        filename = f"uploaded_file_at_{random_id}.txt"
        
        return Material.objects.create(
            **joinkwargs({
                "name": lambda: lorem.text().split(" ")[0],
                "publish_datetime": lambda: datetime.now() + timedelta(days=random.randint(1, 10)),
                "file": lambda: SimpleUploadedFile(
                    filename,
                    (lorem.paragraph() * 3).encode(),
                    "text/plain"
                ),
                **cls.Create_lesson_argument(lesson, kwargs.pop("lesson_date", None))
            }, kwargs)
        )
