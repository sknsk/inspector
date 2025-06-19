"""Python equivalent of server/src/mcpProxy.ts."""

from mcp.shared.message import SessionMessage
from typing import Any, Awaitable, Callable
import anyio

class Transport:
    """Minimal transport interface used by the proxy."""

    def __init__(self, read_stream, write_stream, session_id: str | None = None):
        self.read_stream = read_stream
        self.write_stream = write_stream
        self.session_id = session_id

    async def send(self, message: SessionMessage) -> None:
        await self.write_stream.send(message)

async def mcp_proxy(transport_to_client: Transport, transport_to_server: Transport) -> None:
    async with anyio.create_task_group() as tg:
        async def forward(src: Transport, dest: Transport) -> None:
            async for message in src.read_stream:
                if isinstance(message, Exception):
                    continue
                await dest.send(message)

        tg.start_soon(forward, transport_to_client, transport_to_server)
        tg.start_soon(forward, transport_to_server, transport_to_client)
