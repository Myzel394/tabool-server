from typing import *

from django.db.models import Model

from ._data import related_managers

__all__ = [
    "post_save_manager"
]


def post_save_manager(instance, sender: Type[Model], **kwargs):
    manager_classes = related_managers[sender]
    
    for manager_class in manager_classes:
        manager = manager_class(instance, **kwargs)
        manager.create_relations()
