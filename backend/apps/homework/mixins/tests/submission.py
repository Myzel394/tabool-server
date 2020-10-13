import random
import string

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.lesson.mixins.tests import LessonTestMixin
from apps.utils import joinkwargs
from ...models import Submission

__all__ = [
    "SubmissionTestMixin"
]


class SubmissionTestMixin(LessonTestMixin):
    @classmethod
    def Create_submission(cls, **kwargs) -> Submission:
        random_id = "".join(random.choices(string.ascii_letters + string.digits, k=4))
        
        return Submission.objects.create(
            **joinkwargs(
                {
                    "associated_user": cls.Create_user,
                    "lesson": cls.Create_lesson,
                    "file": lambda: SimpleUploadedFile(
                        f"uploaded_file_{random_id}.txt",
                        "".join(random.choices(string.ascii_letters + string.digits, k=1024 * 5)).encode(),
                        "text/plain"
                    )
                },
                kwargs
            )
        )
