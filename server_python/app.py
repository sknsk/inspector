#!/usr/bin/env python3
"""Simplified Python version of the MCP proxy server."""

import asyncio
import json
import os
import secrets
import uuid
from typing import Dict, Optional
import aiohttp
import anyio
from anyio import create_memory_object_stream
from anyio.abc import TaskGroup
from contextlib import AsyncExitStack

from mcp.client.streamable_http import streamablehttp_client
from mcp.server.streamable_http import StreamableHTTPServerTransport

from .mcp_proxy import Transport, mcp_proxy
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from sse_starlette.sse import EventSourceResponse

# Default environment handling
_default_env = os.environ.copy()
if os.getenv("MCP_ENV_VARS"):
    try:
        _default_env.update(json.loads(os.getenv("MCP_ENV_VARS")))
    except Exception:
        pass

DEFAULT_ENVIRONMENT = _default_env

# Authentication setup
SESSION_TOKEN = secrets.token_hex(32)
AUTH_DISABLED = bool(os.getenv("DANGEROUSLY_OMIT_AUTH"))

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["mcp-session-id"],
)

# In-memory transport registries
_processes: Dict[str, asyncio.subprocess.Process] = {}
_sessions: Dict[str, ProxySession] = {}

class ProxySession:
    """Manage a streamable HTTP proxy session."""

    def __init__(self, url: str, headers: dict[str, str]):
        self.url = url
        self.headers = headers
        self.transport = StreamableHTTPServerTransport(uuid.uuid4().hex)
        self.exit_stack = AsyncExitStack()
        self.task_group: TaskGroup | None = None

    @property
    def session_id(self) -> str:
        return self.transport.mcp_session_id  # type: ignore[arg-type]

    async def start(self) -> None:
        self.task_group = await self.exit_stack.enter_async_context(anyio.create_task_group())
        client_streams = await self.exit_stack.enter_async_context(self.transport.connect())
        self.client_read, self.client_write = client_streams
        server_ctx = streamablehttp_client(self.url, headers=self.headers)
        server_streams = await self.exit_stack.enter_async_context(server_ctx)
        self.server_read, self.server_write, _ = server_streams
        transport_client = Transport(self.client_read, self.client_write, self.session_id)
        transport_server = Transport(self.server_read, self.server_write, None)
        self.task_group.start_soon(mcp_proxy, transport_client, transport_server)

    async def close(self) -> None:
        if self.task_group:
            self.task_group.cancel_scope.cancel()
        await self.exit_stack.aclose()

    async def handle(self, request: Request) -> Response:
        send_stream, receive_stream = create_memory_object_stream(0)

        async def send(message):
            await send_stream.send(message)

        await self.transport.handle_request(request.scope, request.receive, send)

        async def body_iter():
            more_body = True
            status = 200
            headers: list[tuple[bytes, bytes]] = []
            first = True
            while more_body:
                message = await receive_stream.receive()
                if message["type"] == "http.response.start":
                    status = message["status"]
                    headers.extend(message.get("headers", []))
                elif message["type"] == "http.response.body":
                    more_body = message.get("more_body", False)
                    data = message.get("body", b"")
                    if first:
                        first_headers = {k.decode(): v.decode() for k, v in headers}
                        first_headers.setdefault("mcp-session-id", self.session_id)
                        yield status, first_headers, data
                        first = False
                    else:
                        yield None, None, data
            await receive_stream.aclose()

        generator = body_iter()
        status, headers, chunk = await generator.__anext__()
        async def streamer():
            yield chunk
            async for _, _, chunk in generator:
                yield chunk

        return StreamingResponse(streamer(), status_code=status, headers=headers)

async def auth_check(request: Request):
    """Simple bearer token authentication."""
    if AUTH_DISABLED:
        return
    auth_header = request.headers.get("x-mcp-proxy-auth")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header[7:]
    if not secrets.compare_digest(token, SESSION_TOKEN):
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/config")
async def config():
    return {
        "defaultEnvironment": DEFAULT_ENVIRONMENT,
        "defaultCommand": "",
        "defaultArgs": "",
    }


@app.get("/stdio")
async def stdio(request: Request, command: str, args: str = "", env: str = ""):
    await auth_check(request)
    session_id = str(uuid.uuid4())
    cmd_args = [command] + (args.split() if args else [])
    proc_env = DEFAULT_ENVIRONMENT.copy()
    if env:
        try:
            proc_env.update(json.loads(env))
        except Exception:
            pass
    proc = await asyncio.create_subprocess_exec(
        *cmd_args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        env=proc_env,
    )
    _processes[session_id] = proc

    async def event_generator():
        try:
            while True:
                line = await proc.stdout.readline()
                if not line:
                    break
                yield {
                    "event": "message",
                    "data": line.decode(),
                }
        finally:
            _processes.pop(session_id, None)

    headers = {"mcp-session-id": session_id}
    return EventSourceResponse(event_generator(), headers=headers)

@app.get("/sse")
async def sse(request: Request, url: str):
    await auth_check(request)
    session_id = str(uuid.uuid4())
    import aiohttp

    async def event_generator():
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                async for line in resp.content:
                    yield {"event": "message", "data": line.decode()}
    headers = {"mcp-session-id": session_id}
    return EventSourceResponse(event_generator(), headers=headers)


def _extract_headers(request: Request) -> dict[str, str]:
    return {
        key: value
        for key, value in request.headers.items()
        if key.lower() in {"authorization", "mcp-session-id", "last-event-id"}
    }


@app.post("/mcp")
async def mcp_post(request: Request):
    await auth_check(request)
    session_id = request.headers.get("mcp-session-id")
    if session_id and session_id in _sessions:
        session = _sessions[session_id]
    else:
        url = request.query_params.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="url required")
        session = ProxySession(url, _extract_headers(request))
        await session.start()
        _sessions[session.session_id] = session
    return await session.handle(request)


@app.get("/mcp")
async def mcp_get(request: Request):
    await auth_check(request)
    session_id = request.headers.get("mcp-session-id")
    if not session_id or session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = _sessions[session_id]
    return await session.handle(request)


@app.delete("/mcp")
async def mcp_delete(request: Request, sessionId: Optional[str] = None):
    await auth_check(request)
    if sessionId and sessionId in _sessions:
        session = _sessions.pop(sessionId)
        await session.close()
        return Response(status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=404, detail="Session not found")





if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "6277"))
    print(f"Proxy server listening on {host}:{port}")
    if not AUTH_DISABLED:
        print(f"Session token: {SESSION_TOKEN}")
    uvicorn.run("server_python.app:app", host=host, port=port, log_level="info")
