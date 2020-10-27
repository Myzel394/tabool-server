from threading import Thread
from typing import *

__all__ = [
    "run_in_thread"
]


def run_in_thread(target: Callable, args: Iterable = None, kwargs: dict = None, daemonic: bool = True) -> Thread:
    args = args or []
    kwargs = kwargs or {}
    
    thread = Thread(target=target, args=args, kwargs=kwargs)
    thread.setDaemon(daemonic)
    thread.start()
    
    return thread
