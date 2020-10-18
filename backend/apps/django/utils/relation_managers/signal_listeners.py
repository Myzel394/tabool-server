from typing import *

from django.db.models import Model

from ._data import related_managers, related_relation_managers

__all__ = [
    "post_save_manager", "post_save_user_manager", "post_save_related_manager"
]


def update_related_managers_relations(instance, **kwargs):
    manager_classes = related_managers[instance.__class__]
    
    for manager_class in manager_classes:
        manager = manager_class(instance, **kwargs)
        manager.create_relations()


def post_save_manager(instance, **kwargs):
    update_related_managers_relations(instance, **kwargs)


def post_save_user_manager(instance, *args, **kwargs):
    for manager_classes in related_managers.values():
        for manager_class in manager_classes:
            manager_class.create_relations_with_given_user(instance)


def post_save_related_manager(instance, sender: Type[Model], created: bool, **kwargs):
    if created:
        for manager_class in related_relation_managers[sender]:
            model_instance = manager_class.get_model_from_related_instance(instance)
            update_related_managers_relations(model_instance, **kwargs)