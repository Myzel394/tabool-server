from datetime import datetime
from typing import *

from apps.django.utils.send_notification import send_notification

if TYPE_CHECKING:
    from ..models import Homework

__all__ = [
    "push_homework_added"
]


def push_homework_added(homework: "Homework") -> None:
    if homework.due_date and homework.due_date < datetime.now():
        return

    users = homework.lesson.course.user_participants
    subject_name = homework.lesson.course.subject.name

    message_parts = []

    if homework.due_date:
        message_parts.append(f"Die Hausaufgabe ist bis zum {homework.due_date.strftime('%d.%m.%Y')} auf.")
    if homework.type:
        message_parts.append(f"Typ: {homework.type}")

    send_notification(
        users=users,
        collapse_group_name=f"homework_{homework.id}",
        title=f"Es wurde eine neue Hausaufgabe in {subject_name} eingestellt!",
        body="\n".join(message_parts),
        data={
            "type": "homework",
            "payload": {
                "id": homework.id
            }
        }
    )
