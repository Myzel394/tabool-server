from typing import *

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from ...public import *

__all__ = [
    "AccessTokenQuerySet"
]


class AccessTokenQuerySet(BaseUserManager):
    def from_user(self, user: "USER") -> "AccessTokenQuerySet":
        return self.only("user").filter(user=user)
