from django.conf import settings
from django.contrib.auth import get_user_model

from apps.django.authentication.user.choices import GenderChoices
from apps.django.main.event.mixins import ExamTestMixin, ModificationTestMixin
from apps.django.main.homework.mixins import ClassbookTestMixin, HomeworkTestMixin

if settings.DEBUG:
    from dotenv import load_dotenv
    import random
    import string
    import names

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
    from apps.django.main.timetable.mixins import joinkwargs, LessonTestMixin, TimetableTestMixin


    def get_set_values(model, field):
        return set(model.objects.all().values_list(field, flat=True))


    def create_user(confirm: bool = True, staff: bool = False):
        load_dotenv()
        User_model = get_user_model()

        password = "".join(random.choices(string.ascii_letters + string.digits, k=8))

        user = User_model.objects.create_user(
            email=f"{names.get_first_name()}@gmail.com",
            password=password,
            first_name=names.get_first_name(),
            last_name=names.get_last_name(),
            gender=random.choice(GenderChoices.values)  # nosec
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
            HomeworkTestMixin.Create_homework(lesson=random.choice(lessons))  # nosec

        for _ in range(10):
            ClassbookTestMixin.associated_student = student
            ClassbookTestMixin.associated_teacher = teacher

            url = None

            if random.randint(1, 10) >= 7:  # nosec
                url = "https://example.com/test/"

            ClassbookTestMixin.Create_classbook(
                lesson=random.choice(lessons),  # nosec
                video_conference_link=url
            )

        for _ in range(10):
            ModificationTestMixin.associated_student = student
            ModificationTestMixin.associated_teacher = teacher

            ModificationTestMixin.Create_modification(
                lesson=random.choice(lessons),  # nosec
            )

        for _ in range(10):
            ExamTestMixin.associated_student = student
            ExamTestMixin.associated_teacher = teacher

            ExamTestMixin.Create_exam(

                course=random.choice(Course.objects.all())  # nosec
            )


    def create_teacher(**kwargs) -> Teacher:
        teacher = Teacher.objects.create(**joinkwargs({
            "user": lambda: create_user(confirm=True, staff=True),
            "short_name": lambda: "SHT"
        }, kwargs))

        return teacher


    def create_student(**kwargs) -> Student:
        student = Student.objects.create(**joinkwargs({
            "user": lambda: create_user(confirm=True),
            "class_number": lambda: random.randint(5, 13),  # nosec
            "main_teacher": create_teacher,
        }, kwargs))

        return student


    def create_test_env():
        print("CREATING STAFF / TEACHER")

        teacher = create_teacher()

        print("CREATING STUDENT")

        student = create_student(main_teacher=teacher)

        create_timetable(student.user, teacher.user)
