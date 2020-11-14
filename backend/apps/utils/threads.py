from threading import Thread
from typing import *

__all__ = [
    "run_in_thread", "list_in_thread"
]


def run_in_thread(target: Callable, args: Iterable = None, kwargs: dict = None, daemonic: bool = True) -> Thread:
    args = args or []
    kwargs = kwargs or {}
    
    thread = Thread(target=target, args=args, kwargs=kwargs)
    thread.setDaemon(daemonic)
    thread.start()
    
    return thread


def list_in_thread(
        data: Iterable,
        target: Callable,
        extra_args: list = None,
        kwargs: dict = None,
        daemonic: bool = True
) -> None:
    extra_args = extra_args or []
    kwargs = kwargs or {}
    
    threads = []
    
    for element in data:
        thread = Thread(target=target, args=(element, *extra_args), kwargs=kwargs)
        thread.setDaemon(daemonic)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
