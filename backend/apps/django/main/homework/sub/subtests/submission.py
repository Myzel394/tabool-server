from apps.django.main.homework.mixins import SubmissionTestMixin


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
