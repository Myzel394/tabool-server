from django.core.exceptions import ValidationError

from apps.django.main.authentication.models import Token
from apps.django.utils.tests_mixins import UserTestMixin


class TokenTest(UserTestMixin):
    def setUp(self) -> None:
        self.token = Token.objects.create()
    
    def test_cant_change_token(self):
        # Create a new token, otherwise the change fails because the token isn't valid
        new_token = Token.objects.create()
        
        with self.assertRaises(ValidationError):
            self.token.token = new_token.token
            self.token.save()
    
    def test_can_change_user(self):
        user = self.Create_user()
        
        self.token.user = user
        self.token.save()
