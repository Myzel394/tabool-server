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
    def Create_submission(self, **kwargs) -> Submission:
        random_id = "".join(random.choices(string.ascii_letters + string.digits, k=4))
        
        return Submission.objects.create(
            **joinkwargs(
                {
                    "associated_user": self.Create_user,
                    "lesson": self.Create_lesson,
                    "file": lambda: SimpleUploadedFile(
                        f"Hausaufgabe_{random_id}.txt",
                        "".join(random.choices(string.ascii_letters + string.digits, k=1024 * 5)).encode(),
                        "text/plain"
                    )
                },
                kwargs
            )
        )
