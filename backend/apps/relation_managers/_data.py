from collections import defaultdict
from typing import *

from django.db.models import Model

from .managers import RelationManagerMixin, SimpleRelatedRelationManagerMixin

# Dict[ModelClass, List of RelationManagerClasses]
related_managers: Dict[Type[Model], List[Type[RelationManagerMixin]]] = defaultdict(list)

# Dict[RelatedModelClass, List of RelationManagerClasses (of the original Model)]
related_relation_managers: Dict[Type[Model], List[Type[SimpleRelatedRelationManagerMixin]]] = defaultdict(list)
