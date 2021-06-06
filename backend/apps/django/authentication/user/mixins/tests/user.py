import random
import string
from typing import *

import names

from apps.django.authentication.user.choices import GenderChoices
from apps.django.authentication.user.constants import STUDENT, TEACHER
from apps.django.authentication.user.models import Student, Teacher, User
from apps.django.utils.tests_mixins import ClientTestMixin, joinkwargs


class UserTestMixin(ClientTestMixin):
    @classmethod
    def Create_student_user(cls, **kwargs) -> User:
        user = cls.Create_user(**kwargs)
        cls.Create_student(user=user)

        return user

    @classmethod
    def Create_teacher_user(cls, **kwargs) -> User:
        user = cls.Create_user(**kwargs)
        cls.Create_teacher(user=user)

        return user

    @staticmethod
    def Create_user(confirm_email: bool = True, **kwargs) -> User:
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        password = kwargs.pop("password", first_name)

        user = User.objects.create_user(
            **joinkwargs({
                "first_name": lambda: first_name,
                "last_name": lambda: last_name,
                "email": lambda: f"{first_name}.{last_name}@gmail.com",
                "password": lambda: password,
                "gender": lambda: random.choice(GenderChoices.values)
            }, kwargs)
        )

        if confirm_email:
            user.confirm_email(user.confirmation_key)

        return user

    @classmethod
    def Create_student(cls, **kwargs) -> Student:
        return Student.objects.create(
            **joinkwargs({
                "class_number": lambda: random.randint(5, 13),
                "main_teacher": cls.Create_teacher
            }, kwargs)
        )

    @classmethod
    def Create_teacher(cls, **kwargs) -> Teacher:
        first_name = names.get_first_name()

        return Teacher.objects.create(
            **joinkwargs({
                "user": cls.Create_user,
                "short_name": lambda: first_name[:3],
            }, kwargs)
        )

    @staticmethod
    def Get_random_password(level: str = "strong") -> str:
        if level == "weak":
            return random.choice(string.ascii_letters + string.digits) * random.choice([2, 5, 12, 20])
        return "".join(
            random.choices(
                string.ascii_letters + string.digits,
                k=random.choice([12, 14, 20, 24])
            )
        )

    def Login_user(
            self,
            user: Optional[User] = None,
            password: Optional[str] = None,
            user_type: Union[STUDENT, TEACHER] = STUDENT
    ) -> User:
        """Logs the client in and returns the user with which the client was logged in"""
        if not user:
            if user_type == STUDENT:
                user = self.Create_student_user()
            elif user_type == TEACHER:
                user = self.Create_teacher_user()

        is_authenticated = self.client.login(
            email=user.email,
            password=password or user.first_name
        )

        self.assertTrue(is_authenticated, "Couldn't login the user")

        return user

    def Login_student(self) -> User:
        return self.Login_user(user_type=STUDENT)

    def Login_teacher(self) -> User:
        return self.Login_user(user_type=TEACHER)
