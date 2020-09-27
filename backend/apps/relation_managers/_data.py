from collections import defaultdict
from typing import *

from django.db.models import Model

from .managers import RelationManagerMixin

related_managers: Dict[Type[Model], List[Type[RelationManagerMixin]]] = defaultdict(list)
