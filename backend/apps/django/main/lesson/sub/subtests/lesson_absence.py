from apps.django.main.lesson.mixins.tests import LessonAbsence, LessonAbsenceTestMixin, QueryType
from apps.django.main.lesson.sub.subfilters import AbsenceFilterSet
from apps.django.utils.tests_mixins import ClientTestMixin


class LessonAbsenceCreateTest(LessonAbsenceTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.user = self.Login_user()
        self.__class__.associated_user = self.user
    
    def test_create(self):
        lesson = self.Create_lesson()
        
        response = self.client.post("/api/data/lesson-absence/", {
            "lesson": lesson.id,
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
    
    def test_create_not_participant(self):
        lesson = self.Create_lesson()
        course = lesson.course
        course.participants.remove(self.user)
        course.save()
        
        response = self.client.post("/api/data/lesson-absence/", {
            "lesson": lesson.id,
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)


class LessonAbsenceUpdateTest(LessonAbsenceTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.user = self.Login_user()
        self.__class__.associated_user = self.user
        self.absence = self.Create_lesson_absence()
    
    def test_update(self):
        lesson = self.Create_lesson()
        
        response = self.client.patch(f"/api/data/lesson-absence/{self.absence.id}/", {
            "lesson": lesson.id,
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
    
    def test_update_not_participant(self):
        lesson = self.Create_lesson()
        course = lesson.course
        course.participants.remove(self.user)
        course.save()
        
        absence_lesson = self.absence.lesson
        response = self.client.patch(f"/api/data/lesson-absence/{self.absence.id}/", {
            "lesson": lesson.id,
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.absence.refresh_from_db()
        self.assertEqual(absence_lesson, self.absence.lesson)
    
    def test_delete(self):
        response = self.client.delete(f"/api/data/lesson-absence/{self.absence.id}/")
        self.assertStatusOk(response.status_code)


class FilterTest(LessonAbsenceTestMixin):
    def setUp(self) -> None:
        self.user = self.Create_user()
        self.__class__.associated_user = self.user
        self.with_reason = self.Create_lesson_absence(
            reason="test"
        )
        self.without_reason = self.Create_lesson_absence(
            reason=None
        )
    
    @property
    def absences(self) -> QueryType["LessonAbsence"]:
        return LessonAbsence.objects.all()
    
    def test_filters_reason_isnull(self):
        filtered = AbsenceFilterSet({
            "contains_reason": False,
        }, queryset=self.absences)
        
        self.assertIn(self.without_reason, filtered.qs)
        self.assertNotIn(self.with_reason, filtered.qs)
    
    def test_filters_not_reason_isnull(self):
        filtered = AbsenceFilterSet({
            "contains_reason": True,
        }, queryset=self.absences)
        
        self.assertNotIn(self.without_reason, filtered.qs)
        self.assertIn(self.with_reason, filtered.qs)
