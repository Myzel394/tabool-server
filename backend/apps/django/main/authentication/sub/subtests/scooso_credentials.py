import os

from apps.django.utils.tests_mixins import ClientTestMixin, DummyUser, UserTestMixin


class ScoosoCredentialsTest(UserTestMixin, DummyUser, ClientTestMixin):
    def setUp(self):
        if os.getenv("GITHUB_WORKFLOW"):
            return
        
        self.user = self.Login_user()
        self.__class__.associated_user = self.user
    
    def test_get(self):
        if os.getenv("GITHUB_WORKFLOW"):
            return
        
        response = self.client.get("/api/auth/scooso-credentials/")
        self.assertStatusOk(response.status_code)
        self.assertEqual(self.username, response.data["username"])
    
    def test_same_password_change(self):
        if os.getenv("GITHUB_WORKFLOW"):
            return
        
        response = self.client.put("/api/auth/scooso-credentials/", {
            "username": self.username,
            "password": self.password
        }, content_type="application/json")
        self.assertEqual(202, response.status_code)
    
    def test_change_password(self):
        if os.getenv("GITHUB_WORKFLOW"):
            return
        
        # Change password now, so it can be changed via request and 400 doesn't occur
        scooso_data = self.user.scoosodata
        scooso_data.password = ""
        scooso_data.save()
        
        response = self.client.put("/api/auth/scooso-credentials/", {
            "username": self.username,
            "password": self.password
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
    
    def test_invalid_change_password(self):
        if os.getenv("GITHUB_WORKFLOW"):
            return
        
        response = self.client.put("/api/auth/scooso-credentials/", {
            "username": self.username,
            "password": "a"
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
