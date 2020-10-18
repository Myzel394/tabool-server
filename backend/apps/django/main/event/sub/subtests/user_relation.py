from apps.django.main.event.mixins.tests import *
from apps.django.utils.tests import *


class UserRelationTest(UserTestMixin, EventTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
        
        self.event = self.Create_event()
    
    def test_get(self):
        response = self.client.get(
            f"/api/data/event/{self.event.id}/"
        )
        self.assertStatusOk(response.status_code)
