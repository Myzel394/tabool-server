import importlib
import inspect
from typing import *

from django.apps import AppConfig, apps
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from ._data import related_managers, related_relation_managers
from .signal_listeners import post_save_manager, post_save_related_manager, post_save_user_manager

if TYPE_CHECKING:
    from .managers import RelationManagerMixin, SimpleRelatedRelationManagerMixin


class RelationManagersConfig(AppConfig):
    name = "apps.django.utils.relation_managers"
    
    @staticmethod
    def configure_manager(manager: Type["RelationManagerMixin"]):
        model = manager.Meta.model
        related_managers[model].append(manager)
        
        post_save.connect(
            post_save_manager,
            sender=model
        )
    
    @classmethod
    def configure_relation_manager(cls, manager: Type["SimpleRelatedRelationManagerMixin"]):
        model = manager.related_model
        related_relation_managers[model].append(manager)
        
        post_save.connect(
            post_save_related_manager,
            sender=model
        )
    
    @staticmethod
    def configure_user_model():
        post_save.connect(
            post_save_user_manager,
            sender=get_user_model()
        )
    
    def ready(self):
        from .managers import RelationManagerMixin, SimpleRelatedRelationManagerMixin
        
        name: str
        app: AppConfig
        for name, app in apps.app_configs.items():
            try:
                module = importlib.import_module(f"{app.name}.relation_managers")
            except ModuleNotFoundError:
                continue
            
            for element_name in dir(module):
                element = getattr(module, element_name)
                
                if inspect.isclass(element):
                    if issubclass(element, RelationManagerMixin):
                        self.configure_manager(element)
                    
                    if issubclass(element, SimpleRelatedRelationManagerMixin):
                        self.configure_relation_manager(element)
        
        self.configure_user_model()
