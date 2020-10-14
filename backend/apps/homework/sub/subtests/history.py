from apps.homework.mixins.tests.homework import HomeworkTestMixin
from apps.utils import ClientTestMixin
from project.urls import API_VERSION


class HistoryTest(HomeworkTestMixin, ClientTestMixin):
    def test_history(self):
        with self.Login_user_as_context() as _:
            self.homework = self.Create_homework()
            response = self.client.patch(
                f"/api/{API_VERSION}/data/homework/{self.homework.id}/",
                {
                    "information": "Das ist der erste Edit!"
                },
                content_type="application/json"
            )
            self.homework.refresh_from_db()
            
            self.assertStatusOk(response.status_code)
