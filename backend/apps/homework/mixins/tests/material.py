import random
import string

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
        random_id = "".join(random.choices(string.ascii_letters + string.digits, k=5))
        filename = f"uploaded_file_at_{random_id}.txt"
        
        material = Material.objects.create(
            **joinkwargs(
                {
                    "lesson": cls.Create_lesson,
                    "name": lambda: filename,
                    "file": lambda: SimpleUploadedFile(
                        filename,
                        (lorem.paragraph() * 3).encode(),
                        "text/plain"
                    )
                },
                kwargs
            )
        )
        
        return material
