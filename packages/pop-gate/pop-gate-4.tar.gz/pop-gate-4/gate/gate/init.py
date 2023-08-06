from typing import List


def __init__(hub):
    hub.pop.sub.load_subdirs(hub.gate, recurse=True)


def cli(hub):
    hub.pop.config.load(["gate"], cli="gate")
    hub.pop.loop.create()
    coro = hub.gate.init.start(
        gate_server=hub.OPT.gate.server,
        host=hub.OPT.gate.host,
        port=hub.OPT.gate.port,
        matcher_plugin=hub.OPT.gate.matcher,
        prefix=hub.OPT.gate.prefix,
        refs=hub.OPT.gate.refs,
    )
    hub.pop.Loop.run_until_complete(coro)


async def start(
    hub,
    gate_server: str,
    host: str,
    port: int,
    matcher_plugin: str,
    prefix: str,
    refs: List[str],
):
    return await hub.gate.srv[gate_server].start(
        host=host, port=port, matcher_plugin=matcher_plugin, prefix=prefix, refs=refs
    )


async def stop(hub, gate_server: str):
    hub.log.debug("Shutting down gate server")
    return await hub.gate.srv[gate_server].stop()


async def join(hub, gate_server):
    return await hub.gate.srv[gate_server].join()


async def test(hub, *args, **kwargs):
    """
    The test function for gate
    """
    return {"args": args, "kwargs": kwargs}
