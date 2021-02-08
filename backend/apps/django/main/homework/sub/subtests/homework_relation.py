from apps.django.main.homework.mixins import HomeworkTestMixin
from apps.django.main.homework.models import UserHomeworkRelation


class StudentHomeworkUserRelationTest(HomeworkTestMixin):
    def setUp(self):
        self.user = self.Login_student()
        self.__class__.associated_student = self.user
        self.homework = self.Create_homework()
    
    def test_get_when_not_changed(self):
        response = self.client.get(f"/api/student/homework/{self.homework.id}/")
        self.assertStatusOk(response.status_code)
        # Check returned value is default value
        default_value = UserHomeworkRelation._meta.get_field("completed").default
        self.assertEqual(default_value, response.data["user_relation"]["completed"])
    
    def test_change_relation(self):
        response = self.client.patch(f"/api/user-relation/homework/{self.homework.id}/", {
            "completed": True,
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.assertEqual(True, response.data["completed"])
        relation: UserHomeworkRelation = UserHomeworkRelation.objects.all()[0]
        self.assertEqual(True, relation.completed)
