from threading import Thread
from typing import *

__all__ = [
    "run_in_thread"
]


def run_in_thread(
        target: Callable,
        daemonic: bool = False,
        args: Optional[list] = None,
        kwargs: Optional[dict] = None,
) -> Thread:
    args = args or []
    kwargs = kwargs or {}
    
    thread = Thread(target=target, args=args, kwargs=kwargs)
    thread.setDaemon(daemonic)
    thread.start()
    
    return thread
