import random
import string
from datetime import datetime

import lorem
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.django.main.homework.models import Material
from apps.django.main.lesson.mixins.tests import *
from apps.django.utils.tests import *

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
                    "_original_filename": lambda: filename,
                    "file": lambda: SimpleUploadedFile(
                        filename,
                        (lorem.paragraph() * 3).encode(),
                        "text/plain"
                    ),
                    "added_at": lambda: datetime.now()
                },
                kwargs
            )
        )
        
        return material
