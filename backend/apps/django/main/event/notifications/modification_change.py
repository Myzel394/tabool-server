from datetime import datetime
from typing import *

from apps.django.utils.send_notification import send_notification

if TYPE_CHECKING:
    from ..models import Modification

__all__ = [
    "push_modification_change"
]


def push_modification_change(modification: "Modification") -> None:
    if modification.end_datetime < datetime.now():
        return
    
    users = modification.lesson.course.participants.all()
    subject_name = modification.lesson.course.subject.name
    diff_datetime = modification.start_datetime - datetime.now()
    
    message_parts = []
    
    if modification.new_subject:
        message_parts.append(f"Fach: {subject_name} -> {modification.new_subject.name}")
    if modification.new_teacher:
        teacher = modification.lesson.course.teacher
        teacher_name = f"{teacher.first_name} {teacher.last_name}"
        new_teacher_name = f"{modification.new_teacher.first_name} {modification.new_teacher.last_name}"
        message_parts.append(f"Lehrer: {teacher_name} -> {new_teacher_name}")
    if modification.new_room:
        place_name = modification.lesson.room.place
        message_parts.append(f"Raum: {place_name} -> {modification.new_room.place}")
    
    send_notification(
        users=users,
        title=f"Veränderungen am {modification.start_datetime.strftime('%d.%m.%Y')} in {subject_name}!",
        body=f"Es gibt Veränderungen in {subject_name}!" + "\n\n" + "\n".join(message_parts),
        collapse_group_name=f"modification_{modification.id}",
        max_retry_time=int(diff_datetime.total_seconds()),
        is_important=True,
        data={
            "type": "modification",
            "payload": {
                "lesson_id": modification.lesson.id,
                "id": modification.id
            }
        }
    )
