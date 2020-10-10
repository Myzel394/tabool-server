import random
import string
from pathlib import Path

import lorem
from django.conf import settings

from apps.homework.models import build_material_upload_to, Material
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
                },
                kwargs
            )
        )
        path = Path(build_material_upload_to(material, filename))
        path.parent.mkdir(exist_ok=True, parents=True)
        path.touch(exist_ok=True)
        path.write_bytes((lorem.paragraph() * 3).encode())
        material.file = str(path.relative_to(settings.MEDIA_ROOT))
        material.save()
        
        return material
