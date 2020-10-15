import random
import string
from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.lesson.mixins.tests import LessonTestMixin
from apps.lesson.models import LessonScoosoData
from apps.scooso_scraper.scrapers.material import MaterialRequest, MaterialTypeOptions
from apps.utils import ClientTestMixin
from project.urls import API_VERSION


class UploadTest(ClientTestMixin, LessonTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_use = self.logged_user
    
    def test_direct_scooso_upload(self):
        time_id = 29743
        targeted_date = date(2020, 10, 1)
        lesson = self.Create_lesson(
            date=targeted_date
        )
        lesson_scooso_data = LessonScoosoData(
            lesson=lesson,
            time_id=time_id
        )
        lesson.refresh_from_db()
        filename = "upload_test_" + "".join(random.choices(string.ascii_letters + string.digits, k=5)) + ".txt"
        data = "".join(random.choices(string.ascii_letters + string.digits, k=1024 * 5))
        
        response = self.client.post(
            f"/api/{API_VERSION}/data/submission/upload-directly/",
            {
                "lesson": lesson.id,
                "file": SimpleUploadedFile(
                    filename,
                    data.encode()
                )
            }
        )
        self.assertStatusOk(response.status_code)
        
        # Check
        with MaterialRequest(username=self.username, password=self.password) as scraper:
            materials = scraper.get_materials(
                time_id=self.time_id,
                targeted_date=self.target_date,
                material_type=MaterialTypeOptions.HOMEWORK
            )
        
        available_filenames = [
            material['filename']
            for material in materials['materials']
        ]
        self.assertIn(filename, available_filenames)
