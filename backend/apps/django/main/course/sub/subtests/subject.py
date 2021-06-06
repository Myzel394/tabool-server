from apps.django.main.course.mixins import SubjectTestMixin, UserTestMixin
from apps.django.main.course.models import UserSubjectRelation


class SubjectModelTest(SubjectTestMixin, UserTestMixin):
    def test_autofill_color(self):
        user = self.Create_user()
        subject = self.Create_subject()

        UserSubjectRelation.objects.create(
            user=user,
            subject=subject
        )


class SubjectAPITest(SubjectTestMixin, UserTestMixin):
    def setUp(self):
        self.Login_student()
        self.Create_subject()

    def test_get(self):
        response = self.client.get("/api/student/subject/")
        self.assertStatusOk(response.status_code)
