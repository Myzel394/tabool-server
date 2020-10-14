from apps.event.mixins.tests.event import EventTestMixin
from apps.utils import ClientTestMixin, UserTestMixin
from project.urls import API_VERSION


class UserRelationTest(UserTestMixin, EventTestMixin, ClientTestMixin):
    def setUp(self) -> None:
        self.logged_user = self.Login_user()
        self.__class__.associated_user = self.logged_user
        
        self.event = self.Create_event()
    
    def test_get(self):
        response = self.client.get(
            f"/api/{API_VERSION}/data/event/{self.event.id}/"
        )
        self.assertStatusOk(response.status_code)
