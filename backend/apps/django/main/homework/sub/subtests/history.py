from pprint import pp

from apps.django.main.homework.mixins.tests import HomeworkTestMixin
from apps.django.utils.tests import *


class HistoryTest(HomeworkTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
        
        self.first_content = "First Edit!"
        self.second_content = "Second Edit!"
        
        self.homework = self.Create_homework(private_to_user=self.logged_user)
        response = self.client.patch(
            f"/api/data/homework/{self.homework.id}/",
            {"information": self.first_content},
            content_type="application/json"
        )
        self.assertStatusOk(response.status_code)
        response = self.client.patch(
            f"/api/data/homework/{self.homework.id}/",
            {"information": self.second_content},
            content_type="application/json"
        )
        self.assertStatusOk(response.status_code)
    
    def test_get_history(self):
        response = self.client.get(f"/api/data/homework/{self.homework.id}/history/")
        self.assertStatusOk(response.status_code)
        
        pp(response.data)
        first_edit = response.data["results"][0]
        response = self.client.get(f"/api/data/homework/{self.homework.id}/history/{first_edit['pk']}/")
        self.assertStatusOk(response.status_code)
        pp(response.data)
