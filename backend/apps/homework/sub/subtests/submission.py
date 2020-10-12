import random
import string
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.homework.mixins.tests.submission import SubmissionTestMixin
from apps.utils import ClientTestMixin


class SubmissionTest(SubmissionTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
    
    def test_api_get(self):
        submission = self.Create_submission()
        
        response = self.client.get("/api/submission/")
        self.assertStatusOk(response.status_code)
        
        response = self.client.get(f"/api/submission/{submission.id}/")
        self.assertStatusOk(response.status_code)
    
    def test_api_post(self):
        lesson = self.Create_lesson()
        file = SimpleUploadedFile(
            "file.txt",
            "".join(random.choices(string.ascii_letters + string.digits, k=1024 * 5)).encode(),
            "text/plain"
        )
        
        path = Path("/tmp/tabool/test.txt")
        path.parent.mkdir(exist_ok=True, parents=True)
        path.touch(exist_ok=True)
        path.write_text("".join(random.choices(string.ascii_letters + string.digits, k=1024 * 5)))
        
        with path.open() as opened_file:
            response = self.client.post(
                "/api/submission/",
                {
                    "lesson": lesson.id,
                    "file": opened_file
                },
                content_type="multipart/form-data"
            )
        print(response.data)
        self.assertStatusOk(response.status_code)  # Error
