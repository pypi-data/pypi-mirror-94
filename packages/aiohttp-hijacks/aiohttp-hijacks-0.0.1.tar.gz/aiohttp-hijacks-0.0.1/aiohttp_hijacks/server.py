import socket

import aiohttp
import aiohttp.resolver
import aiohttp.test_utils
import aiohttp.web


def get_unused_port():
    return aiohttp.test_utils.unused_port()


class FakeResolver(object):
    """ aiohttp resolver that hijacks a set of uris """

    def __init__(self, fakes):
        self.fakes = fakes
        self.resolver = aiohttp.resolver.DefaultResolver()

    async def resolve(self, host, port=0, family=socket.AF_INET):
        """ make dns resolution : google.com -> 127.0.0.1
        Raise an error if host isn't rerouted => never perform requests to the scary internet
        """
        fake_port = self.fakes.get(host)
        if fake_port is not None:
            return [{
                "hostname": host,
                "host": "127.0.0.1",
                "port": fake_port,
                "family": socket.AF_INET,
                "proto": 0,
                "flags": socket.AI_NUMERICHOST,
            }]
        raise OSError(f"Fake DNS lookup failed: no fake server known for {host}")


class FakeSession(aiohttp.ClientSession):
    """ aiohttp session that filters out ssl urls """

    def __init__(self, *args, **kwargs):
        """ resolver does translation 'google.com' -> '127.0.0.1' or raise error if host not
        rerouted
        """
        resolver = FakeResolver(kwargs.pop("reroute"))
        kwargs["connector"] = aiohttp.TCPConnector(resolver=resolver)
        super().__init__(*args, **kwargs)

    async def _request(self, method, url, **kwargs):
        """ re-write request method to remove any ssl """

        # if not string then get string from yarl.URL object
        url = str(url)
        if url.startswith("https"):
            url = "http" + url[5:]
        elif url.startswith("wss"):
            url = "ws" + url[3:]
        return await super()._request(method, url, **kwargs)


def route(path, method="get"):
    """ decorator to add attributes to FakeServer instances """

    def decorator(fn):
        fn.path = path
        fn.method = method
        return fn

    return decorator


class FakeServer:
    """ Fake server listening on unused port
    usage example

    ::
        class Server(FakeServer):
            @route('/') # the decorator set attributes path & method -> required by
                                        FakeServer
            async def get_abc(self, request):
                self.calls += 1
                return self.json_response({"status": "ok"})

        async with Server() as server: # instantiate Server handling '127.0.0.1:{server.port}/abc'
            async with FakeSession(reroute={'google.com': server.port}) as session:
                # redirecting calls to http(s)://google.com to 127.0.0.1:{server.port}
                reply = await session.get("https://google.com).json()
                assert reply == {"status": "ok"}
    """

    async def __aenter__(self):
        """ require to be use in async white FakeServer() as server: ..."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        """ require to be use in async white FakeServer() as server: ..."""
        await self.stop()

    async def start(self):
        """ Select an unused port and start a web server listening on it """
        self.calls = 0
        self.requests = []
        self.port = get_unused_port()
        self.app = aiohttp.web.Application()
        for key in dir(self):
            value = getattr(self, key)
            if callable(value) and hasattr(value, "path") and hasattr(value, "method"):
                self.app.router.add_route(value.method, value.path, value)
        self.runner = aiohttp.web.AppRunner(self.app)
        await self.runner.setup()
        site = aiohttp.web.TCPSite(self.runner, "127.0.0.1", self.port)
        await site.start()

    async def stop(self):
        """ stop the web server """
        await self.runner.cleanup()

    @property
    def url(self):
        return f"http://127.0.0.1:{self.port}"

    @staticmethod
    def json_response(data):
        """ Return aiohttp.web.json_response from dict. """
        return aiohttp.web.json_response(data)
