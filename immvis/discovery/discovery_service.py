from core.service import Service
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
from string import Template
import asyncio

_MAGIC = "U2bhY3XUOli9GgdUGs9ruxuXKpuj78Qi3zNT5IEkiQy5ex4UxqXZ5ZDAj9vkTyVz2GZiFXDS4bY5Ayve2HrAiB7G2jN7d5rskERyj3b5GeQAv1PYEOdD5sys"

class DiscoveryService(Service):
    _should_broadcast = False
    _task = None

    def __init__(self, port=5000, delay=5, magic=_MAGIC):
        Service.__init__(self)
        self._port = port
        self._delay = delay
        self._magic = magic

    def start(self):
        _should_broadcast = True
        loop = asyncio.get_event_loop()
        self._task = loop.create_task(self._broadcast)

    def stop(self):
        _should_broadcast = False

        if self._task is not None:
            self._task.cancel()
            self._task = None

    async def _broadcast(self):
        broadcast_socket = socket(AF_INET, SOCK_DGRAM)
        broadcast_socket.bind(('', 0))
        broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        current_ip = gethostbyname(gethostname())

        while self._should_broadcast:
            data = Template("$magic:$ip").substitute(
                magic=_MAGIC, ip=current_ip)
            broadcast_socket.sendto(str.encode(
                data), ('<broadcast>', self._port))

            try:
                await asyncio.sleep(self._delay)
            except asyncio.CancelledError:
                break

        return