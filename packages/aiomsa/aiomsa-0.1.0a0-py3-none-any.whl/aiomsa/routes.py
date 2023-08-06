#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

import json
import logging

from aiohttp import web

from .utils.dict import deep_update


routes = web.RouteTableDef()


@routes.get("/status")
async def handle_get_status(request: web.Request) -> web.Response:
    """Check if the webserver is responsive.

    Args:
        request: Request context injected by :mod:`aiohttp`.

    Returns:
        "Alive" text indicating that the webserver is healthy.

    Example:
        ::

            # curl -i http://localhost:8080/status
            HTTP/1.1 200 OK
            Content-Type: text/plain; charset=utf-8
            Content-Length: 5
            Date: Tue, 12 May 2020 18:57:45 GMT
            Server: Python/3.8 aiohttp/3.6.2

            Alive

    ---
    description: Check if the webserver is responsive.
    tags:
    - Health
    produces:
    - text/plain
    responses:
      "200":
        description: Successful operation. Return "Alive" text.
    """
    return web.Response(text="Alive")


@routes.get("/config")
async def handle_get_config(request: web.Request) -> web.Response:
    """Return the current service configuration settings.

    Args:
        request: Request context injected by :mod:`aiohttp`.

    Returns:
        The service's current configuration settings.

    Raises:
        web.HTTPInternalServerError: Failed to load or parse the configuration file.

    Example:
        ::

            # curl -i http://localhost:8080/config
            HTTP/1.1 200 OK
            Content-Type: application/json; charset=utf-8
            Content-Length: 56
            Date: Tue, 12 May 2020 18:59:12 GMT
            Server: Python/3.8 aiohttp/3.6.2

            {"foo": ["bar", "baz"], "timeout": 15}

    ---
    description: Return the current service configuration settings.
    tags:
    - Configuration
    produces:
    - application/json
    responses:
      "200":
        description: Successful operation.
      "500":
        description: Failed to load or parse the configuration file.
    """
    try:
        with open("./service_config.json") as f:
            config = json.load(f)
            return web.json_response(config)
    except json.JSONDecodeError:
        raise web.HTTPInternalServerError(
            text="Existing configuration is not valid JSON"
        )
    except OSError:
        raise web.HTTPInternalServerError(text="Failed to load existing configuration")


@routes.put("/config")
async def handle_set_config(request: web.Request) -> web.Response:
    """Completely overwrite the service's configuration settings.

    Args:
        request: Request context injected by :mod:`aiohttp`.

    Returns:
        The overwritten configuration settings.

    Raises:
        web.HTTPBadRequest: Missing or invalid input ``config`` parameter.
        web.HTTPInternalServerError: Failed to overwrite service configuration.

    Example:
        ::

            # curl -id '{"foo": ["bar", "baz"], "timeout": 15}' http://localhost:8080/config -X PUT
            HTTP/1.1 200 OK
            Content-Type: application/json; charset=utf-8
            Content-Length: 56
            Date: Tue, 12 May 2020 19:00:57 GMT
            Server: Python/3.8 aiohttp/3.6.2

            {"foo": ["bar", "baz"], "timeout": 15}

    ---
    description: Completely overwrite the service's configuration settings.
    tags:
    - Configuration
    produces:
    - application/json
    parameters:
    - in: body
      name: config
      description: New service configuration object
      required: true
      schema:
        type: object
        properties:
          config:
            type: object
        required:
        - config
    responses:
      "200":
        description: Successful operation.
      "400":
        description: Missing or invalid 'config' parameter.
      "500":
        description: Failed to overwrite service configuration.
    """
    body = await request.json()

    if "config" not in body:
        raise web.HTTPBadRequest(text="Missing required 'config' param")

    config = body["config"]
    if not isinstance(config, dict):
        raise web.HTTPBadRequest(text="Invalid value for 'config': Not object")

    try:
        with open("./service_config.json", "w") as f:
            json.dump(config, f)

        # Trigger the shutdown event
        request.app["shutdown_event"].set()
        return web.json_response(config)
    except OSError:
        raise web.HTTPInternalServerError(text="Failed to overwrite config")


@routes.patch("/config")
async def handle_update_config(request: web.Request) -> web.Response:
    """Partially update the service's configuration settings.

    Args:
        request: Request context injected by :mod:`aiohttp`.

    Returns:
        The updated configuration settings.

    Raises:
        web.HTTPBadRequest: Missing or invalid ``config`` parameter.
        web.HTTPInternalServerError: Failed to update service configuration.

    Example:
        ::

            # curl -id '{"config": {"timeout": 30}}' http://localhost:8080/config -X PATCH
            HTTP/1.1 200 OK
            Content-Type: application/json; charset=utf-8
            Content-Length: 56
            Date: Tue, 12 May 2020 19:00:57 GMT
            Server: Python/3.8 aiohttp/3.6.2

            {"foo": ["bar", "baz"], "timeout": 30}

    ---
    description: Partially update the service's configuration settings.
    tags:
    - Configuration
    produces:
    - application/json
    parameters:
    - in: body
      name: config
      description: Partial service configuration object with updated values.
      required: true
      schema:
        type: object
        properties:
          config:
            type: object
        required:
        - config
    responses:
      "200":
        description: Successful operation.
      "400":
        description: Missing or invalid 'config' parameter.
      "500":
        description: Failed to update service configuration.
    """
    body = await request.json()

    if "config" not in body:
        raise web.HTTPBadRequest(text="Missing required 'config' param")

    updates = body["config"]
    if not isinstance(updates, dict):
        raise web.HTTPBadRequest(text="Invalid value for 'config': Not object")

    try:
        with open("./service_config.json", "r+") as f:
            config = json.load(f)
            deep_update(config, updates)

            # Write new config at the beginning of the file and truncate what's left
            f.seek(0)
            json.dump(config, f)
            f.truncate()

        # Trigger the shutdown event
        request.app["shutdown_event"].set()
        return web.json_response(config)
    except json.JSONDecodeError:
        raise web.HTTPInternalServerError(
            text="Existing configuration is not valid JSON"
        )
    except OSError:
        raise web.HTTPInternalServerError(text="Failed to update configuration")


@routes.put("/log/{level:[A-Z]+}")
async def handle_set_log_level(request: web.Request) -> web.Response:
    """Dynamically set the service's log level.

    Args:
        request: Request context injected by :mod:`aiohttp`.

    Returns:
        Text response indicating that the log level was properly set.

    Raises:
        web.HTTPBadRequest: Invalid log level.

    Example:
        ::

            # curl -i http://localhost:8080/log/WARNING -X PUT
            HTTP/1.1 200 OK
            Content-Type: text/plain; charset=utf-8
            Content-Length: 34
            Date: Tue, 12 May 2020 19:06:34 GMT
            Server: Python/3.8 aiohttp/3.6.2

            Log level set to WARNING from INFO

    ---
    description: Dynamically set the service's log level.
    tags:
    - Configuration
    produces:
    - text/plain
    parameters:
    - in: path
      name: level
      description: The new log level.
      required: true
      type: string
      enum: [DEBUG, INFO, WARNING, ERROR, FATAL]
    responses:
      "200":
        description: Successful operation.
      "400":
        description: Invalid log level.
    """
    level = request.match_info["level"]
    prev_level = logging.getLevelName(logging.root.level)

    if level == prev_level:
        return web.Response(text=f"Log level is already {prev_level}")

    try:
        logging.root.setLevel(level)
    except ValueError as e:
        raise web.HTTPBadRequest(text=str(e))

    return web.Response(text=f"Log level set to {level} from {prev_level}")
