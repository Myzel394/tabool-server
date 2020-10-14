import random
import string
from datetime import date
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.authentication.models import ScoosoData
from apps.homework.mixins.tests.submission import SubmissionTestMixin
from apps.lesson.models import LessonScoosoData
from apps.scooso_scraper.mixins.tests.dummy_data import DummyUser
from apps.scooso_scraper.scrapers.material import MaterialRequest, MaterialTypeOptions
from apps.utils import ClientTestMixin


class SubmissionTest(SubmissionTestMixin, ClientTestMixin, DummyUser):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
        self.load_dummy_user()
    
    def test_api_get(self):
        submission = self.Create_submission()
        
        response = self.client.get("/api/submission/")
        self.assertStatusOk(response.status_code)
        
        response = self.client.get(f"/api/submission/{submission.id}/")
        self.assertStatusOk(response.status_code)
    
    def test_api_post(self):
        DATA = "".join(random.choices(string.ascii_letters + string.digits, k=1024 * 5)).encode()
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
        
        lesson = self.Create_lesson()
        
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
                "/api/submission/",
                data={
                    "lesson": lesson.id,
                    "file": SimpleUploadedFile(
                        "file.txt",
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


class ApiTest(SubmissionTestMixin, ClientTestMixin, DummyUser):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
        self.load_dummy_user()
        
        self.time_id = 29743
        self.target_date = date(2020, 10, 1)
        
        user_scooso_data = ScoosoData.objects.create(
            user=self.logged_user,
            username=self.username,
            password=self.password
        )
        
        self.lesson = self.Create_lesson(
            date=self.target_date
        )
        scooso_data = LessonScoosoData.objects.create(
            lesson=self.lesson,
            time_id=self.time_id
        )
    
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
            f"/api/submission/{submission.id}/upload/"
        )
        self.assertStatusOk(response.status_code)
        self.assertEqual(response.data["upload_status"], "RESTING")
        
        response = self.client.post(
            f"/api/submission/{submission.id}/upload/"
        )
        self.assertStatusOk(response.status_code)
        self.assertEqual(response.data["upload_status"], "UPLOADED")
    
    def test_upload_api_second(self):
        submission = self.Create_submission(
            lesson=self.lesson,
            associated_user=self.logged_user
        )
        submission.upload_file()
        
        response = self.client.get(
            f"/api/submission/{submission.id}/upload/"
        )
        self.assertStatusOk(response.status_code)
        self.assertEqual(response.data["upload_status"], "UPLOADED")
        
        response = self.client.post(
            f"/api/submission/{submission.id}/upload/"
        )
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["upload_status"], "UPLOADED")
