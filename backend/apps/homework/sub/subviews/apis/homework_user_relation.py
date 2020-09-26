from apps.utils.viewsets import UserRelationViewSetMixin
from ....models import Homework
from ....serializers import UserHomeworkRelationSerializer


class UserHomeworkRelationViewSet(UserRelationViewSetMixin):
    serializer_class = UserHomeworkRelationSerializer
    model = Homework
