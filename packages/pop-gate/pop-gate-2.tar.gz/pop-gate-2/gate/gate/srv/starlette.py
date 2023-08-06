# Import python libs
import asyncio
import traceback
from typing import List

try:
    # Import third party libs
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route
    from starlette.requests import Request
    from uvicorn import Server
    from uvicorn.config import Config

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


async def start(
    hub, host: str, port: int, matcher_plugin: str, prefix: str, refs: List[str]
):
    async def _query(request):
        return await hub.gate.srv.starlette.query(
            request, prefix=prefix, refs=refs, matcher_plugin=matcher_plugin
        )

    routes = [
        Route("/", _query, methods=["GET", "POST", "PUT"]),
    ]
    app = Starlette(debug=True, routes=routes)
    config = Config(app, host=host, port=port, loop="none")
    hub.gate.srv.starlette.SERVER = Server(config)

    return await hub.gate.srv.starlette.SERVER.serve()


async def join(hub):
    """
    Block until the server has started
    """
    while not hasattr(hub.gate.srv.starlette, "SERVER"):
        await asyncio.sleep(0, loop=hub.pop.Loop)

    while not getattr(hub.gate.srv.starlette.SERVER, "started", False):
        await asyncio.sleep(0, loop=hub.pop.Loop)

    # Wait just one more cycle for everything to start
    await asyncio.sleep(0, loop=hub.pop.Loop)


async def stop(hub):
    hub.gate.srv.starlette.SERVER.should_exit = True
    hub.gate.srv.starlette.SERVER.force_exit = True
    await hub.gate.srv.starlette.SERVER.shutdown()


async def query(
    hub, request: Request, matcher_plugin: str, prefix: str, refs: List[str]
) -> JSONResponse:
    if request.headers["Content-type"] == "application/json":
        q_params = await request.json()
    else:
        q_params = dict(request.query_params)

    if "ref" not in q_params:
        return JSONResponse(
            {"error": "Required ref not found in params"}, status_code=417
        )

    q_ref = q_params.get("ref")
    if prefix:
        q_ref = f"{prefix}.{q_ref}"

    if not hub.gate.matcher[matcher_plugin].match(q_ref, prefix=prefix, refs=refs):
        return JSONResponse(
            {"error": f"The provided ref {q_ref} is not available for execution"},
            status_code=405,
        )

    if not hasattr(hub, q_ref):
        return JSONResponse(
            {"error": f"The provided ref {q_ref} does not exist"}, status_code=404
        )

    try:
        ret = await hub.gate.srv.init.runner(
            q_ref, *q_params.get("args", []), **q_params.get("kwargs", {}),
        )
        return JSONResponse(ret, status_code=200)
    except Exception as e:
        hub.log.error(traceback.format_exc())
        return JSONResponse(
            {"error": f"hub.{q_ref} returned {e.__class__.__name__}: {e}"},
            status_code=500,
        )
