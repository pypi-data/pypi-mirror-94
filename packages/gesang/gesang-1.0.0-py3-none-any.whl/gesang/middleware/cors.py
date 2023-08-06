from starlette.middleware.cors import CORSMiddleware
from gesang.middleware.base import BaseMiddleware


class CorsMiddleware(BaseMiddleware):
    default_options = {
        "allow_origins": (),
        "allow_methods": ("GET", "POST", "PUT", "DELETE"),
        "allow_headers": (),
        "allow_credentials": True,
        "allow_origin_regex": None,
        "expose_headers": (),
        "max_age": 600
    }
    settings_name = "CORS_SETTINGS"
    middleware_cls = CORSMiddleware
