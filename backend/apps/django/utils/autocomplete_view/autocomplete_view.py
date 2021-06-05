from abc import ABC, abstractmethod
from typing import *

from django_hint import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.django.utils.autocomplete_view.exceptions import InvalidQueryError
from apps.django.utils.autocomplete_view.type_hints import DefaultResultType

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User

__all__ = [
    "AutocompleteView", ]

T = TypeVar("T")


class AutocompleteView(APIView, ABC, Generic[T]):
    throttle_scope = "autocomplete"
    model: StandardModelType
    user: "User"
    
    def is_user_allowed(self, user: "User") -> bool:  # skipcq: PYL-R0201
        return True
    
    @abstractmethod
    def get_qs(self, user: "User") -> T:
        raise NotImplementedError()
    
    @abstractmethod
    def filter_qs(self, qs: T, query: str) -> T:
        raise NotImplementedError()
    
    @abstractmethod
    def serialize_qs(self, qs: T) -> list[DefaultResultType]:
        raise NotImplementedError()
    
    def validate_query(self, query: str) -> None:
        pass
    
    def is_query_valid(self, query: str) -> bool:  # skipcq: PYL-R0201
        return query != ""
    
    def get(self, request: RequestType):
        user = request.user
        
        if not self.is_user_allowed(user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        qs = self.get_qs(user)
        query = request.GET.get("q", "")
        
        try:
            self.validate_query(query)
        except InvalidQueryError as error:
            return Response({
                "detail": error.message,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        filtered_qs = self.filter_qs(qs, query)
        
        response = self.serialize_qs(filtered_qs)
        
        return Response({
            "results": response
        })
