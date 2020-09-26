from apps.lesson.mixins.tests import RoomTestMixin
from apps.utils import ClientTestMixin, UserCreationTestMixin


class APITest(ClientTestMixin, UserCreationTestMixin, RoomTestMixin):
    def setUp(self) -> None:
        for _ in range(500):
            self.Create_room()
    
    def test_pagination(self):
        with self.Login_user_as_context() as user:
            response = self.client.get("/api/room/")
            
            print(response.data)
