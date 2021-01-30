from pathlib import Path
from typing import *

from django_common_utils.libraries.utils import create_short

from apps.django.utils.send_notification import send_notification

if TYPE_CHECKING:
    from apps.django.main.homework.models import Submission


def push_submission_scooso_upload_failed(submission: "Submission"):
    subject = submission.lesson.course.subject.name
    path = Path(submission.file.path)
    
    send_notification(
        users=[submission.associated_user],
        collapse_group_name=f"submission_scooso_upload_failed_{submission.id}",
        title=f"Deine Datei \"{create_short(path.name, 20)}\" in {subject} konnte nicht hochgeladen werden!",
        data={
            "type": "submission_scooso_upload_failed",
            "payload": {
                "lesson_id": submission.lesson.id
            }
        }
    )


def push_submission_scooso_upload_succeeded(submission: "Submission"):
    subject = submission.lesson.course.subject.name
    path = Path(submission.file.path)
    
    send_notification(
        users=[submission.associated_user],
        collapse_group_name=f"submission_scooso_upload_succeeded_{submission.id}",
        title=f"Deine Datei \"{create_short(path.name, 20)}\" in {subject} wurde erfolgreich hochgeladen!",
        data={
            "type": "submission_scooso_upload_succeeded",
            "payload": {
                "lesson_id": submission.lesson.id
            }
        }
    )
