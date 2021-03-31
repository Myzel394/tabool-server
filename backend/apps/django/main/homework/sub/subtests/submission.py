import time
from datetime import datetime, timedelta

from apps.django.main.homework.mixins import SubmissionTestMixin
from apps.django.main.homework.models import Submission
from apps.django.utils.tests_mixins import GenericAPITestMixin


class StorageTest(SubmissionTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_student = self.student
        
        self.submission = self.Create_submission()
        self.url = self.submission.file.url
    
    def test_correct_student_can_access(self):
        response = self.client.get(self.url)
        self.assertStatusOk(response.status_code)
    
    def test_wrong_user_can_not_access(self):
        self.client.logout()
        self.Login_student()
        
        response = self.client.get(self.url)
        self.assertStatusNotOk(response.status_code)
    
    def test_correct_teacher_can_access(self):
        # Make teacher
        teacher = self.Login_teacher()
        course = self.submission.lesson.course
        
        course.teacher = teacher.teacher
        course.save()
        
        response = self.client.get(self.url)
        self.assertStatusOk(response.status_code)
    
    def test_wrong_teacher_can_not_access(self):
        self.Login_teacher()
        
        response = self.client.get(self.url)
        self.assertStatusNotOk(response.status_code)
    
    def test_unauthenticated_user_can_not_access(self):
        self.client.logout()
        
        response = self.client.get(self.url)
        self.assertStatusNotOk(response.status_code)


class SubmissionAPITest(SubmissionTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_student = self.student
        self.submission = self.Create_submission()
    
    def test_get(self):
        response = self.client.get(f"/api/student/submission/")
        self.assertStatusOk(response.status_code)
    
    def test_cant_edit_publish_datetime_when_already_published(self):
        self.submission.publish_datetime = datetime.now() - timedelta(days=2)
        self.submission.save()
        
        response = self.client.patch(f"/api/student/submission/{self.submission.id}/", {
            "publish_datetime": datetime.now() + timedelta(days=1)
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
    
    def test_can_edit_publish_datetime_when_not_published(self):
        self.submission.publish_datetime = datetime.now() + timedelta(days=1)
        self.submission.save()
        
        response = self.client.patch(f"/api/student/submission/{self.submission.id}/", {
            "publish_datetime": datetime.now() + timedelta(days=2)
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)


class StudentSubmissionAPITest(SubmissionTestMixin, GenericAPITestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.__class__.associated_student = self.student
    
    def test_can_upload(self):
        submission = self.Create_submission()
        
        response = self.client.post(f"/api/student/submission/{submission.id}/upload/")
        self.assertEqual(200, response.status_code)
    
    def test_can_not_upload_already_uploaded(self):
        submission = self.Create_submission()
        submission.publish_datetime = datetime.now() - timedelta(days=1)
        submission.save()
        
        response = self.client.post(f"/api/student/submission/{submission.id}/upload/")
        self.assertEqual(202, response.status_code)
    
    def test_can_access(self):
        self.generic_access_test(
            obj=self.Create_submission(),
            api_suffix="student/"
        )


class TeacherSubmissionAPITest(SubmissionTestMixin, GenericAPITestMixin):
    def setUp(self):
        self.__class__.associated_teacher = self.Login_teacher()
    
    def test_can_access(self):
        submission = self.Create_submission(
            publish_datetime=datetime.now() + timedelta(seconds=3)
        )
        time.sleep(3)
        
        self.generic_access_test(
            obj=submission,
            api_suffix="teacher/"
        )
    
    def test_can_not_do_lifecycle_methods(self):
        self.generic_lifecycle_test(
            model=Submission,
            post_data={},
            patch_data={},
            api_suffix="teacher/",
            should_be_ok=False,
            foreign_obj=self.Create_submission()
        )
