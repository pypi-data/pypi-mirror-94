import asyncio
from typing import Any, Dict, Tuple, List


def __init__(hub):
    # A mapping of dyne_names/subs to a reference to a function on the hub that should run that function
    # If no reference is listed then a getattr(hub, ref) will be done and the reference will be called directly
    hub.gate.srv.RUNNER = {}


async def runner(hub, ref: str, *args, **kwargs) -> Any:
    """
    Call a function based on runners defined before the program started
    """
    prefix = ref.split(".")[0]
    if prefix in hub.gate.srv.RUNNER:
        func = hub.gate.srv.RUNNER[prefix]
        if not hasattr(func, "__call__"):
            # If the prefix was a string then get it's reference on the hub
            func = hub[func]
    else:
        func = hub[ref]

    if args and kwargs:
        ret = func(ref, *args, **kwargs)
    elif args:
        ret = func(ref, *args)
    elif kwargs:
        ret = func(ref, **kwargs)
    else:
        ret = func(ref)

    if asyncio.iscoroutine(ret):
        return await ret
    return ret
