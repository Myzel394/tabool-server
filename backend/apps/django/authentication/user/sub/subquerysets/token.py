from typing import *

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from ...public import *

__all__ = [
    "TokenQuerySet"
]


class TokenQuerySet(BaseUserManager):
    def from_user(self, user: "USER") -> "TokenQuerySet":
        return self.only("user").filter(user=user)
