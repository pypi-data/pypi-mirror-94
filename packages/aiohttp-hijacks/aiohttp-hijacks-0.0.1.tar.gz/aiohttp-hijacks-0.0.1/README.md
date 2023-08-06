aiohttp-hijacks
===

Hijack aiohttp session to re-route the requests.

```py
from aiohttp_hijacks import FakeServer, FakeSession, route


class Server(FakeServer):
    """ Application that will respond to the client. """
    @route('/')
    async def get_abc(self, request):
        self.calls += 1
        return self.json_response({"status": "ok"})


# Reroute google.com → 127.0.0.1
async with Server() as server:  # instantiate Server handling '127.0.0.1:{server.port}/abc'
    async with FakeSession(reroute={'google.com': server.port}) as session:
        # redirecting calls to http(s)://google.com to 127.0.0.1:{server.port}
        resp = await session.get("https://google.com")
        data = await resp.json()
        assert data == {"status": "ok"}
```