from django.conf import settings
from django.contrib.auth import get_user_model

from apps.django.main.event.mixins import ExamTestMixin, ModificationTestMixin
from apps.django.main.homework.mixins import ClassbookTestMixin, HomeworkTestMixin

if settings.DEBUG:
    from dotenv import load_dotenv
    import random, string, names
    
    # noinspection PyUnresolvedReferences
    from apps.django.authentication.user.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.authentication.otp.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.authentication.sessions.models import *
    
    # noinspection PyUnresolvedReferences
    from apps.django.main.event.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.main.day.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.main.course.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.main.timetable.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.main.homework.models import *
    
    # noinspection PyUnresolvedReferences
    from apps.django.extra.news.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.extra.poll.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.main.timetable.mixins import LessonTestMixin, TimetableTestMixin
    
    
    def get_set_values(model, field):
        return set(model.objects.all().values_list(field, flat=True))
    
    
    def create_user(confirm: bool = True, staff: bool = False):
        load_dotenv()
        User = get_user_model()
        
        password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        
        user = User.objects.create_user(
            email=f"{names.get_first_name()}@gmail.com",
            password=password
        )
        
        if confirm:
            user.confirm_email(user.confirmation_key)
        if staff:
            user.is_superuser = True
            user.is_staff = True
        
        user.save()
        
        print("Email:", user.email)
        print("Password:", password)
        
        return user
    
    
    def create_timetable(student: User = None, teacher: User = None):
        LessonTestMixin.associated_student = student
        LessonTestMixin.associated_teacher = teacher
        
        LessonTestMixin.Create_whole_timetable()
        lessons = Lesson.objects.all()
        
        for _ in range(10):
            HomeworkTestMixin.associated_student = student
            HomeworkTestMixin.associated_teacher = teacher
            HomeworkTestMixin.Create_homework()
        
        for _ in range(10):
            ClassbookTestMixin.associated_student = student
            ClassbookTestMixin.associated_teacher = teacher
            
            ClassbookTestMixin.Create_classbook(
                lesson=random.choice(lessons),
                video_conference_link="https://bbb.url.com/test/" if random.randint(1, 10) > 8 else None
            )
        
        for _ in range(10):
            ModificationTestMixin.associated_student = student
            ModificationTestMixin.associated_teacher = teacher
            
            ModificationTestMixin.Create_modification(
                lesson=random.choice(lessons),
            )
        
        for _ in range(10):
            ExamTestMixin.associated_student = student
            ExamTestMixin.associated_teacher = teacher
            
            ExamTestMixin.Create_exam(
                course=random.choice(Course.objects.all())
            )
