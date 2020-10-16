from typing import *

from django.contrib.auth.base_user import BaseUserManager

from ...constants import PAY_USER_SAMPLE_AMOUNT
from ...utils import get_school_starts_date_for_year

if TYPE_CHECKING:
    from ...public import USER


__all__ = [
    "UserPaymentQuerySet"
]


class UserPaymentQuerySet(BaseUserManager):
    def filter_not_paid_for_year(self, year: Optional[int]) -> "UserPaymentQuerySet":
        return self.only("paid_at").filter(
            paid_at__lte=get_school_starts_date_for_year(year)
        )
    
    def filter_paid_for_year(self, year: Optional[int]) -> "UserPaymentQuerySet":
        return self.only("paid_at").filter(
            paid_at__gte=get_school_starts_date_for_year(year)
        )
    
    def filter_user_paid_for_year(self, user: "USER", year: Optional[int]) -> "UserPaymentQuerySet":
        return self.filter_paid_for_year(year).only("user").filter(user=user)
    
    def has_user_paid_for_year(self, user: "USER", year: Optional[int]) -> bool:
        return self.filter_user_paid_for_year(user, year).exists()
