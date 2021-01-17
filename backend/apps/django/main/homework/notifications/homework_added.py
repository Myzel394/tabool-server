from typing import *

from apps.django.utils.send_notification import send_notification

if TYPE_CHECKING:
    from ..models import Homework


def push_homework_added(homework: "Homework") -> None:
    users = homework.lesson.lesson_data.course.participants
    subject_name = homework.lesson.lesson_data.course.subject.name
    
    message_parts = []
    
    if homework.due_date:
        message_parts.append(f"Die Hausaufgabe ist bis zum {homework.due_date.strftime('%d.%m.%Y')} auf.")
    if homework.type:
        message_parts.append(f"Typ: {homework.type}")
    
    send_notification(
        users=users,
        collapse_group_name=f"homework_{homework.id}",
        title=f"Es wurde eine neue Hausaufgabe in {subject_name} eingestellt!",
        body="\n".join(message_parts)
    )
