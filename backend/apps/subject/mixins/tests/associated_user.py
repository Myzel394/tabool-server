import re
from abc import ABC

from django.db import models
from django_hint import *

from apps.utils.tests import UserCreationTestMixin


class AssociatedUserTestMixin(UserCreationTestMixin, ABC):
    def check_queryset_from_user(self, model: Type[models.Model], create_func: Optional[Callable] = None):
        # Constraining values
        snake_case_name = re.sub(r'(?<!^)(?=[A-Z])', '_', model.__name__).lower()
        create_func = create_func or getattr(self, f"Create_{snake_case_name}")
        
        previous_value = getattr(self.__class__, "associated_user", None)
        
        self.client.logout()
        user = self.Login_user()
        self.__class__.associated_user = user
        
        # Create one, visible for the user
        create_func()
        
        # Create one, not visible for the user
        # Change user
        self.__class__.associated_user = self.Create_user()
        create_func()
        
        # Cleanup
        self.__class__.associated_user = previous_value
        
        # Check
        self.assertNotEqual(model.objects.all(), model.objects.all().from_user(user))
        self.assertEqual(model.objects.all().count(), 2)
        self.assertEqual(model.objects.all().from_user(user).count(), 1)
