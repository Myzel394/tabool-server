from rest_framework import serializers
from user_sessions.backends.db import SessionStore
from user_sessions.models import Session

__all__ = [
    "SessionSerializer"
]


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = [
            "user_agent", "ip", "last_activity", "is_this", "id"
        ]
        
    id = serializers.SerializerMethodField()
    is_this = serializers.SerializerMethodField()
    
    def get_is_this(self, instance: Session) -> bool:
        request_session: SessionStore = self.context["request"].session
        
        return instance.session_key == request_session.session_key
    
    def get_id(self, instance: Session) -> str:
        return instance.sessionrelation.id
