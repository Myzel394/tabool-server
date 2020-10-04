from datetime import datetime

import lorem
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.homework.models import Material
from apps.lesson.mixins.tests import LessonTestMixin
from apps.utils import joinkwargs

__all__ = [
    "MaterialTestMixin"
]


class MaterialTestMixin(LessonTestMixin):
    @classmethod
    def Create_material(cls, **kwargs) -> Material:
        return Material.objects.create(
            **joinkwargs(
                {
                    "lesson": cls.Create_lesson,
                    "file": lambda: SimpleUploadedFile(
                        f"uploaded_file_at_{datetime.now().strftime('%d_%m_%Y,_%H:%M')}.txt",
                        (lorem.paragraph() * 3).encode()
                    )
                },
                kwargs
            )
        )
