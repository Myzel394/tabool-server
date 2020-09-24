import json
from pprint import pp

import lorem

from apps.homework.mixins.tests.homework import HomeworkTestMixin
from apps.homework.models import TeacherHomework, UserHomework
from apps.homework.sub.subserializers import (
    TeacherHomeworkListSerializer, UserHomeworkDetailSerializer,
    UserHomeworkListSerializer,
)
from apps.subject.mixins.tests.associated_user import AssociatedUserTestMixin
from apps.utils.tests import ClientTestMixin

__all__ = [
    "APITest", "QuerySetTest"
]


class APITest(HomeworkTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
    
    def test_receive_from_lesson(self):
        homework = self.Create_teacher_homework()
        
        response = self.client.get(
            "/api/teacher-homework/"
        )
        
        self.assertEqual(
            json.loads(json.dumps(response.data)),
            json.loads(json.dumps(TeacherHomeworkListSerializer(TeacherHomework.objects.all(), many=True).data))
        )
    
    def test_create_user_homework(self):
        homework = self.Create_user_homework()
        homework.delete()
        
        response = self.client.post(
            "/api/user-homework/",
            UserHomeworkDetailSerializer(homework).data,
            content_type="application/json"
        )
        
        print(response.data)
        self.assertStatusOk(response.status_code)
        
        self.assertTrue(UserHomework.objects.all().exists())
    
    def test_update_user_homework(self):
        homework = self.Create_user_homework()
        new_information = lorem.sentence()
        
        print(UserHomework.objects.from_user(self.logged_user))
        
        response = self.client.patch(
            f"/api/user-homework/{homework.id}/",
            {
                "information": new_information
            },
            content_type="application/json"
        )
        
        print(response.data)
        self.assertStatusOk(response.status_code)
        
        homework.refresh_from_db(fields=["information"])
        self.assertEqual(homework.information, new_information)

    def test_by_subject(self):
        subject = self.Create_subject()
        homeworks = [
            self.Create_user_homework(
                lesson=self.Create_lesson(
                    lesson_data=self.Create_lesson_data(
                        subject=subject
                    )
                )
            )
            for _ in range(5)
        ]
    
        response = self.client.get(
            "/api/user-homework/by-subject/",
            {
                "subject": subject.id
            },
            content_type="application/json"
        )
        
        self.assertStatusOk(response.status_code)
    
        [
            homework.refresh_from_db()
            for homework in homeworks
        ]
        
        expected_data = UserHomeworkListSerializer(homeworks, many=True).data
        actual_data = response.data
    
        self.assertCountEqual(expected_data, actual_data)


class QuerySetTest(HomeworkTestMixin, AssociatedUserTestMixin):
    def test_association(self):
        self.check_queryset_from_user(UserHomework)
        self.check_queryset_from_user(TeacherHomework)
