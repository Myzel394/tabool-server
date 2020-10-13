import random
import string

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
        DATA = "".join(random.choices(string.ascii_letters + string.digits, k=1024 * 5)).encode()
        HTML = """
            <html>
                <body>
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
