from apps.django.main.course.mixins import CourseTestMixin


class CourseAPITest(CourseTestMixin):
    def setUp(self):
        self.student = self.Login_student()
        self.teacher = self.Create_teacher_user()
        self.course = self.Create_course(
            teacher=self.teacher.teacher,
            participants=[self.student.student]
        )
    
    def test_student_gets_correct_serialized_course(self):
        response = self.client.get(f"/api/student/course/{self.course.id}/", )
        self.assertStatusOk(response.status_code)
        
        self.assertIn("participants_count", response.data)
        self.assertNotIn("participants", response.data)
    
    def test_teacher_gets_correct_serialized_course(self):
        self.Login_user(self.teacher, self.teacher.first_name)
        
        response = self.client.get(f"/api/student/course/{self.course.id}/", )
        self.assertStatusOk(response.status_code)
        
        self.assertNotIn("participants_count", response.data)
        self.assertIn("participants", response.data)
