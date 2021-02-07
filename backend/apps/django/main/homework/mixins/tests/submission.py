import random
import string
from datetime import datetime, timedelta

import lorem
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.django.main.homework.models import Submission
from apps.django.main.timetable.mixins import joinkwargs
from .material import MaterialTestMixin

__all__ = [
    "SubmissionTestMixin"
]


class SubmissionTestMixin(MaterialTestMixin):
    @classmethod
    def Create_submission(cls, **kwargs) -> Submission:
        random_id = "".join(random.choices(string.ascii_letters + string.digits, k=5))
        filename = f"uploaded_file_at_{random_id}.txt"
        
        return Submission.objects.create(
            **joinkwargs({
                "name": lambda: lorem.text().split(" ")[0],
                "publish_datetime": lambda: datetime.now() + timedelta(days=random.randint(1, 10)),
                "file": lambda: SimpleUploadedFile(
                    filename,
                    (lorem.paragraph() * 3).encode(),
                    "text/plain"
                ),
                "associated_user": lambda: getattr(cls, "associated_user", None) or cls.Create_user(),
                **cls.Create_lesson_argument()
            }, kwargs)
        )
