from apps.lesson.mixins.tests.course import CourseTestMixin
from apps.lesson.models import Course
from apps.utils import ClientTestMixin


class APITest(ClientTestMixin, CourseTestMixin):
    def test_course(self):
        with self.Login_user_as_context() as user:
            for _ in range(200):
                self.Create_course()
            
            course = Course.objects.all().from_user(user).first()
            
            response = self.client.get(f"/api/course/{course.id}/")
            
            print()
