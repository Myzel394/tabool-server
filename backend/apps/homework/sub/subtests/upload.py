from django.core.files.uploadedfile import SimpleUploadedFile

from apps.lesson.mixins.tests.lesson import LessonUploadTestMixin
from apps.scooso_scraper.scrapers.material import MaterialRequest, MaterialTypeOptions
from apps.utils import ClientTestMixin, UtilsTestMixin
from project.urls import API_VERSION


class UploadTest(ClientTestMixin, LessonUploadTestMixin, UtilsTestMixin):
    def setUp(self) -> None:
        self.load_lesson_upload()
    
    def test_direct_scooso_upload(self):
        filename = self.Random_filename()
        
        response = self.client.post(
            f"/api/{API_VERSION}/data/submission/scooso/",
            {
                "lesson": self.lesson.id,
                "file": SimpleUploadedFile(
                    filename,
                    self.Random_data(1024 * 5).encode()
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
