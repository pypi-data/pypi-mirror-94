from typing import List, Type, Callable
import logging.config

import sentry_sdk
from sentry_sdk.integrations.sanic import SanicIntegration

from macrobase_driver.driver import MacrobaseDriver
from macrobase_driver.logging import get_logging_config
from macrobase_driver.config import CommonConfig, AppConfig

from sanic_macrobase.config import SanicDriverConfig
from sanic_macrobase.route import Route
from sanic_macrobase.hook import SanicHookNames

from structlog import get_logger
from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.handlers import ErrorHandler

log = get_logger('SanicDriver')


class SanicDriver(MacrobaseDriver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.name is None:
            self.name = 'SanicDriver'

        self._routes = []
        self._preload_server()

    @property
    def config(self) -> CommonConfig[AppConfig, SanicDriverConfig]:
        return self._config

    def _preload_server(self):
        if self.config.driver.sentry_dsn:
            sentry_sdk.init(
                dsn=self.config.driver.sentry_dsn,
                integrations=[SanicIntegration()],
                environment=self.config.driver.sentry_env
            )

        self._sanic = Sanic(name=self.name, log_config=get_logging_config(self.config.app))
        self._sanic.config = self.config.driver.get_sanic_config()

    def add_hook(self, name: SanicHookNames, handler):
        """
        Add hook handler

        Args:
            name (SanicHookNames): Enum of hook event
            handler: Function of callback
        """
        super().add_hook(name.value, handler)

    def add_routes(self, routes: List[Route]):
        """
        Add HTTP routes
        """
        self._routes.extend(routes)

    def set_error_handler(self, error_handler: ErrorHandler):
        """
        Set error handler for sanic application
        Args:
            error_handler (ErrorHandler): Instance of error handler
        """
        self._sanic.error_handler = error_handler

    def add_error_handler(self, exception_cls: Type[Exception], func: Callable[[Request, Exception], None]):
        """
        Add error handler function for Exception class type
        Args:
            exception_cls (Type[Exception]): Type of Exception
            func (Callable[[Request, Exception], None]): Function for calling
        """
        self._sanic.error_handler.add(exception_cls, func)

    def _apply_routes(self):
        prefix = self.config.driver.blueprint

        if prefix is None or len(prefix) == 0:
            server = self._sanic
        else:
            server = Blueprint(prefix, url_prefix=prefix)

        if self.config.driver.health_endpoint:
            from .endpoint import HealthEndpoint
            server.add_route(HealthEndpoint(self.context, self.config), '/health', {'GET', 'POST'})

        [server.add_route(
            r.handler,
            r.uri,
            methods=r.methods,
            host=r.host,
            strict_slashes=r.strict_slashes,
            version=r.version,
            name=r.name) for r in self._routes]

        if isinstance(server, Blueprint):
            self._sanic.blueprint(server)

    def _apply_logging(self):
        self._logging_config = get_logging_config(self.config.app)
        logging.config.dictConfig(self._logging_config)

    def _apply_hooks(self):
        for name, handlers in self._hooks.items():
            for handler in handlers:
                self._sanic.listener(name)(handler)

        # async def lock_context(driver, context: Context, loop):
        #     context.lock()
        #
        # self._sanic.listener(SanicHookNames.after_server_start.value)(HookHandler(self, lock_context))
        pass

    def _prepare_server(self):
        self._apply_logging()
        self._apply_hooks()
        self._apply_routes()

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)

        self._prepare_server()

        try:
            self._sanic.run(
                host=self.config.driver.host,
                port=self.config.driver.port,
                workers=self.config.driver.workers,

                debug=self.config.app.debug,
                access_log=self.config.driver.access_log)
        except Exception as e:
            log.error(e)
            self._sanic.stop()
