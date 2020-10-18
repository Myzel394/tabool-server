from django_eventstream.channelmanager import DefaultChannelManager

__all__ = [
    "UserActiveChannelManager"
]


class UserActiveChannelManager(DefaultChannelManager):
    def can_read_channel(self, user, _) -> bool:
        if user is not None \
                and user.is_authenticated \
                and user.is_active \
                and user.has_filled_out_data \
                and user.is_confirmed \
                and user.is_scooso_data_valid:
            return True
        return False
