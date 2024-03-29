from apps.django.authentication.otp.models import OTP
from apps.django.authentication.user.mixins import UserTestMixin


class OTPISValidTest(UserTestMixin):
    def setUp(self) -> None:
        self.user = self.Create_student_user()
        self.otp = OTP.objects.create(
            associated_user=self.user
        )

    def test_is_valid_works_with_correct_token(self):
        self.assertTrue(self.otp.is_valid(self.otp.token))

    def test_is_not_valid_works_with_incorrect_token(self):
        otp = OTP.objects.create(
            associated_user=self.user
        )
        self.assertFalse(self.otp.is_valid(otp.token))
