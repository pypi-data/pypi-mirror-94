from starlette.middleware.gzip import GZipMiddleware
from gesang.middleware.base import BaseMiddleware


class GzipMiddleware(BaseMiddleware):

    default_options = {
        "minimum_size": 500
    }
    settings_name = "GZIP_SETTINGS"
    middleware_cls = GZipMiddleware
