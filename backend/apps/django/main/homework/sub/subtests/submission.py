from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.django.extra.scooso_scraper.scrapers.material import *
from apps.django.main.homework.mixins.tests import *
from apps.django.main.lesson.mixins.tests import *
from apps.django.utils.tests import *
from constants.api import API_VERSION


class SubmissionTest(SubmissionTestMixin, ClientTestMixin, LessonUploadTestMixin, UtilsTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
        self.load_lesson_upload()
    
    def test_api_get(self):
        submission = self.Create_submission(lesson=self.lesson)
        
        response = self.client.get(f"/api/{API_VERSION}/data/submission/")
        self.assertStatusOk(response.status_code)
        
        response = self.client.get(f"/api/{API_VERSION}/data/submission/{submission.id}/")
        self.assertStatusOk(response.status_code)
    
    def test_api_post(self):
        DATA = self.Random_data(1024 * 5).encode()
        HTML = """
            <html>
                <body>
                    <h1>Hello</h1>
                    <h1>Hello</h1>
                    <h1>Hello</h1>
                    <h1>Hello</h1>
                    <h1>Hello</h1>
                    <h1>Hello</h1>
                    <h1>Hello</h1>
                    <h1>Hello</h1>
                    <h1>Hello</h1>
                </body>
            </html>
        """.encode()
        
        for data, mimetype, is_status_ok in (
                (DATA, "text/plain", True),
                (DATA, "image/png", True),
                (DATA, "random_mime_type", True),
                (HTML, "text/html", False),
                (HTML, "text/plain", False),
                (HTML, "image/png", False),
        ):
            print(mimetype)
            response = self.client.post(
                f"/api/{API_VERSION}/data/submission/",
                data={
                    "lesson": self.lesson.id,
                    "file": SimpleUploadedFile(
                        self.Random_filename(),
                        data,
                        mimetype
                    )
                }
            )
            print(response.data)
            if is_status_ok:
                self.assertStatusOk(response.status_code)
            else:
                self.assertStatusNotOk(response.status_code)


class ApiTest(SubmissionTestMixin, ClientTestMixin, LessonUploadTestMixin):
    def setUp(self) -> None:
        self.load_lesson_upload()
    
    def test_upload(self):
        submission = self.Create_submission(
            lesson=self.lesson,
            associated_user=self.logged_user
        )
        
        submission.upload_file()
        
        # Check
        filename = Path(submission.file.path).name
        
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
    
    def test_upload_api(self):
        submission = self.Create_submission(
            lesson=self.lesson,
            associated_user=self.logged_user
        )
        
        response = self.client.get(
            f"/api/{API_VERSION}/data/submission/{submission.id}/upload/"
        )
        self.assertStatusOk(response.status_code)
        self.assertEqual("RESTING", response.data["upload_status"])
        
        response = self.client.post(
            f"/api/{API_VERSION}/data/submission/{submission.id}/upload/"
        )
        self.assertStatusOk(response.status_code)
        self.assertEqual("UPLOADED", response.data["upload_status"])
    
    def test_upload_api_get(self):
        submission = self.Create_submission(
            lesson=self.lesson,
            associated_user=self.logged_user
        )
        submission.upload_file()
        
        response = self.client.get(
            f"/api/{API_VERSION}/data/submission/{submission.id}/upload/"
        )
        self.assertStatusOk(response.status_code)
        self.assertEqual(response.data["upload_status"], "UPLOADED")
        
        response = self.client.post(
            f"/api/{API_VERSION}/data/submission/{submission.id}/upload/"
        )
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["upload_status"], "UPLOADED")
