from apps.django.main.school_data.models import Teacher
from .other_scrapers.scrape_teachers import scrape_teachers

__all__ = [
    "import_teachers"
]


def import_teachers() -> list[Teacher]:
    teachers = scrape_teachers()
    teachers_added = []
    
    for teacher_data in teachers:
        teacher, _ = Teacher.objects.get_or_create(
            short_name=teacher_data['short_name']
        )
        teacher.first_name = teacher_data['first_name']
        teacher.last_name = teacher_data['last_name']
        teacher.email = teacher_data['email']
        teacher.save()
        
        teachers_added.append(teacher)
    
    return teachers_added
