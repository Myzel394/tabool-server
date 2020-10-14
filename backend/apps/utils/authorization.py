from django_eventstream.channelmanager import DefaultChannelManager

__all__ = [
    "UserActiveChannelManager"
]


class UserActiveChannelManager(DefaultChannelManager):
    def can_read_channel(self, user, _) -> bool:
        if user is not None and user.is_authenticated and user.is_confirmed:
            return True
        return False
