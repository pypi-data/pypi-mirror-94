import traceback
from typing import Dict

import aiohttp_cors
from aiohttp import web as aio_web
from aiohttp.web_request import Request
from aiohttp.web_urldispatcher import Resource, ResourceRoute

from bolinette import console, blnt, web
from bolinette.exceptions import APIError, APIErrors, InternalError, InitError
from bolinette.utils.serializing import serialize


class BolinetteResources:
    def __init__(self, context: 'blnt.BolinetteContext'):
        self.context = context
        self._aiohttp_resources: Dict[str, 'BolinetteResource'] = {}
        self._routes: Dict[str, Dict[web.HttpMethod, web.ControllerRoute]] = {}
        self.cors = aiohttp_cors.setup(self.context.app, defaults=self._setup_cors())

    @property
    def routes(self):
        for path, methods in self._routes.items():
            for method, route in methods.items():
                yield path, method, route

    def _setup_cors(self):
        try:
            conf = {}
            if 'cors' in self.context.env:
                conf = self.context.env['cors']
            if not isinstance(conf, dict):
                raise ValueError()
            defaults = {}
            for site, config in conf.items():
                if not isinstance(config, dict):
                    raise ValueError()
                defaults[site] = aiohttp_cors.ResourceOptions(
                    allow_credentials=config.get('allow_credentials', False),
                    expose_headers=config.get('expose_headers', ()),
                    allow_headers=config.get('allow_headers', ())
                )
            return defaults
        except ValueError:
            raise InitError("""
Invalid CORS config, you should have something like:

cors:
  "*":
    allow_credentials: true
    expose_headers: "*"
    allow_headers: "*"
  "http://client.example.org":
    allow_credentials: true
    expose_headers: "*"
    allow_headers: "*"
    max_age: 3600

See https://github.com/aio-libs/aiohttp-cors for detailed config options
""")

    def add_route(self, path: str, controller: 'web.Controller', route: 'web.ControllerRoute'):
        if path not in self._routes:
            self._routes[path] = {}
        self._routes[path][route.method] = route
        if path not in self._aiohttp_resources:
            self._aiohttp_resources[path] = BolinetteResource(self.cors.add(self.context.app.router.add_resource(path)))
        handler = RouteHandler(controller, route)
        self._aiohttp_resources[path].routes[route.method] = self.cors.add(
            self._aiohttp_resources[path].resource.add_route(route.method.http_verb, handler.__call__))


class BolinetteResource:
    def __init__(self, resource: Resource):
        self.resource = resource
        self.routes: Dict[web.HttpMethod, ResourceRoute] = {}


class RouteHandler:
    def __init__(self, controller: 'web.Controller', route: 'web.ControllerRoute'):
        self.controller = controller
        self.route = route

    async def __call__(self, request: Request):
        context: blnt.BolinetteContext = request.app['blnt']
        params = {
            'match': {},
            'query': {},
            'request': request
        }
        for key in request.match_info:
            params['match'][key] = request.match_info[key]
        for key in request.query:
            params['query'][key] = request.query[key]
        try:
            resp = await self.route.call_middleware_chain(request, params)
            return resp
        except (APIError, APIErrors) as ex:
            res = web.Response(context).from_exception(ex)
            if context.env['debug']:
                stack = traceback.format_exc()
                if isinstance(ex, InternalError):
                    console.error(stack)
                res.content['trace'] = stack.split('\n')
            serialized, mime = serialize(res.content, 'application/json')
            web_response = aio_web.Response(text=serialized, status=res.code, content_type=mime)
            return web_response
