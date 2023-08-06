from macrobase_driver.config import DriverConfig, fields

from sanic.config import Config


class SanicDriverConfig(DriverConfig):

    logo = fields.Str("""
 _____       _
|  __ \     (_)               
| |  | |_ __ ___   _____ _ __ 
| |  | | '__| \ \ / / _ \ '__|
| |__| | |  | |\ V /  __/ |   
|_____/|_|  |_| \_/ \___|_|sanic
    """)

    workers = fields.Int(1)

    host = fields.Str('0.0.0.0')
    port = fields.Int(8000)

    blueprint = fields.Str('')
    health_endpoint = fields.Bool(True)

    request_max_size            = fields.Int(100000000)  # 100 megabytes
    request_timeout             = fields.Int(60)  # 60 seconds
    response_timeout            = fields.Int(60)  # 60 seconds
    keep_alive                  = fields.Bool(True)
    keep_alive_timeout          = fields.Int(5)  # 5 seconds
    websocket_max_size          = fields.Int(2 ** 20)  # 1 megabytes
    websocket_max_queue         = fields.Int(32)
    websocket_read_limit        = fields.Int(2 ** 16)
    websocket_write_limit       = fields.Int(2 ** 16)
    graceful_shutdown_timeout   = fields.Int(15.0)  # 15 sec
    access_log                  = fields.Bool(True)

    sentry_dsn                  = fields.Str('', env_key='SENTRY_DSN')
    sentry_env                  = fields.Str('', env_key='SENTRY_ENV')

    def get_sanic_config(self) -> Config:
        c = Config()
        c.LOGO = self.logo
        c.REQUEST_MAX_SIZE = self.request_max_size
        c.REQUEST_TIMEOUT = self.request_timeout
        c.RESPONSE_TIMEOUT = self.response_timeout
        c.KEEP_ALIVE = self.keep_alive
        c.KEEP_ALIVE_TIMEOUT = self.keep_alive_timeout
        c.WEBSOCKET_MAX_SIZE = self.websocket_max_size
        c.WEBSOCKET_MAX_QUEUE = self.websocket_max_queue
        c.WEBSOCKET_READ_LIMIT = self.websocket_read_limit
        c.WEBSOCKET_WRITE_LIMIT = self.websocket_write_limit
        c.GRACEFUL_SHUTDOWN_TIMEOUT = self.graceful_shutdown_timeout
        c.ACCESS_LOG = self.access_log

        return c
