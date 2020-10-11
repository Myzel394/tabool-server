import random
import string
from pathlib import Path

from django.conf import settings

from apps.lesson.mixins.tests import LessonTestMixin
from apps.utils import joinkwargs
from ...models import Submission
from ...public import build_submission_upload_to

__all__ = [
    "SubmissionTestMixin"
]


class SubmissionTestMixin(LessonTestMixin):
    @classmethod
    def Create_submission(cls, **kwargs) -> Submission:
        random_id = "".join(random.choices(string.ascii_letters + string.digits, k=4))
        filename = f"uploaded_file_{random_id}.pdf"
        data = joinkwargs(
            {
                "associated_user": cls.Create_user,
                "lesson": cls.Create_lesson,
            },
            kwargs
        )
        submission_instance = Submission(**data)
        path = Path(build_submission_upload_to(instance=submission_instance, filename=filename))
        submission_instance.file = str(path.relative_to(settings.MEDIA_ROOT))
        submission_instance.save()
        
        return submission_instance
