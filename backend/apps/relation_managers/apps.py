import importlib
import inspect
from typing import *

from django.apps import AppConfig, apps
from django.db.models.signals import post_save

from ._data import related_managers
from .signal_listeners import post_save_manager

if TYPE_CHECKING:
    from .managers import RelationManagerMixin


class RelationManagersConfig(AppConfig):
    name = "apps.relation_managers"
    
    @staticmethod
    def configure_manager(manager: Type["RelationManagerMixin"]):
        model = manager.Meta.model
        related_managers[model].append(manager)
        
        post_save.connect(
            post_save_manager,
            sender=model
        )
    
    def ready(self):
        from .managers import RelationManagerMixin
        
        name: str
        app: AppConfig
        for name, app in apps.app_configs.items():
            try:
                module = importlib.import_module(f"{app.name}.relation_managers")
            except ModuleNotFoundError:
                continue
            
            for element_name in dir(module):
                element = getattr(module, element_name)
                
                if inspect.isclass(element) and issubclass(element, RelationManagerMixin):
                    self.configure_manager(element)
