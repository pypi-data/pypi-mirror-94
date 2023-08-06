#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

__version__ = "2020.12.01"
__all__ = ["init"]

import asyncio
import logging
import os
import signal
from typing import Callable, Optional, cast

from aiohttp import web

from .e2 import E2
from .exceptions import DuplicateRouteError
from .routes import routes


@web.middleware
async def error_middleware(request: web.Request, handler: Callable) -> web.Response:
    """Middleware for returning non-200 responses as JSON."""
    try:
        return cast(web.Response, await handler(request))
    except web.HTTPError as e:
        return web.json_response(
            {"status": "error", "message": e.text}, status=e.status
        )
    except Exception:
        logging.exception("Error handling request")
        return web.json_response(
            {"status": "error", "message": "Server got itself in trouble"}, status=500
        )


def init(  # noqa: C901
    main: Callable,
    extra_routes: Optional[web.RouteTableDef] = None,
    add_metrics_route: bool = False,
    add_swagger_docs: bool = False,
    use_uvloop: bool = False,
    listen_on_ipv6: bool = False,
) -> None:
    """Start the webserver and the entrypoint logic passed in as ``main``.

    Args:
        main: A ``lambda`` function wrapper to the entrypoint for the service's logic.
        extra_routes: Additional endpoints to add to the HTTP server.
        add_metrics_route: Adds an endpoint for Prometheus to scrape metrics.
        add_swagger_docs: Adds Swagger documentation to HTTP routes.
        use_uvloop: Uses the uvloop event loop instead of asyncio's built-in loop.
        listen_on_ipv6: Instructs the webserver to listen on "::" instead of "0.0.0.0".

    Raises:
        DuplicateRouteError: An extra route conflicts in name and method with the
                             default routes.
        RuntimeError: A user-requested runtime dependency is missing.
    """
    logging.basicConfig(
        format="%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Use uvloop to make asyncio fast
    if use_uvloop:
        try:
            import uvloop

            uvloop.install()
        except ImportError:
            raise RuntimeError("uvloop is not installed")

    # Create web application object and shutdown event
    app = web.Application(middlewares=[error_middleware])
    app["main"] = main
    app["shutdown_event"] = asyncio.Event()

    # Initialize routes for the HTTP server
    app.add_routes(routes)

    # Add a /metrics route for exposing Prometheus metrics
    if add_metrics_route:
        try:
            from prometheus_async import aio

            app.router.add_get("/metrics", aio.web.server_stats)
        except ImportError:
            raise RuntimeError("prometheus_async is not installed")

    # Add any extra routes to the HTTP Server
    if extra_routes is not None:
        routes_set = set()
        for route in routes:
            if isinstance(route, web.RouteDef):
                route = cast(web.RouteDef, route)
                routes_set.add((route.method, route.path))

        for route in extra_routes:
            if isinstance(route, web.RouteDef):
                route = cast(web.RouteDef, route)
                if (route.method, route.path) in routes_set:
                    raise DuplicateRouteError(route.method, route.path)

        app.add_routes(extra_routes)

    # Document HTTP API endpoints with swagger
    if add_swagger_docs:
        try:
            from aiohttp_swagger import setup_swagger

            setup_swagger(app)
        except ImportError:
            raise RuntimeError("aiohttp_swagger is not installed")

    app.on_startup.append(_start_background_tasks)
    app.on_cleanup.append(_stop_background_tasks)
    web.run_app(app, host="::" if listen_on_ipv6 else "0.0.0.0")


async def _start_background_tasks(app: web.Application) -> None:
    """Start the E2 and create the main_wrapper and shutdown_listener tasks."""

    await E2.start()
    app["main_wrapper_task"] = asyncio.create_task(_main_wrapper(app))
    app["shutdown_listener_task"] = asyncio.create_task(_shutdown_listener(app))


async def _stop_background_tasks(app: web.Application) -> None:
    """Cancel the shutdown_listener and main_wrapper tasks and stop the E2."""
    try:
        app["shutdown_listener_task"].cancel()
        await app["shutdown_listener_task"]
    except asyncio.CancelledError:
        pass

    if not app["main_wrapper_task"].done():
        try:
            app["main_wrapper_task"].cancel()
            await app["main_wrapper_task"]
        except asyncio.CancelledError:
            pass

    await E2.stop()

    # Raise the exception caught in the main_wrapper if the task wasn't cancelled
    if not app["main_wrapper_task"].cancelled():
        await app["main_wrapper_task"]


async def _main_wrapper(app: web.Application) -> None:
    """Run the supplied 'main' and set the shutdown event if it fails."""
    try:
        await app["main"]()
    except:  # noqa: E722
        app["shutdown_event"].set()
        raise


async def _shutdown_listener(app: web.Application) -> None:
    """Wait for the shutdown_event notification to kill the process."""
    await app["shutdown_event"].wait()
    logging.info("Shutting down!")

    # Sleep for 1 second before terminating
    await asyncio.sleep(1)
    os.kill(os.getpid(), signal.SIGTERM)
