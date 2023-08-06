from starlette.applications import Starlette
from gesang.conf.settings import settings
from gesang.utils.funcs import load_middleware, load_module_class_string
from gesang.url.conf import UrlManager
from gesang.plugin.base import BasePlugin


class Gesang:

    def __init__(self):
        self.__app = Starlette()

    def init_app(self):
        # 加载中间件
        self.__load_middlewares()
        # 加载插件
        self.__load_plugins()
        # 加载路由配置
        UrlManager().init_app(app=self.__app)

    def __load_middlewares(self):
        """
        加载中间件
        :return:
        """
        for middlewares_module_class_path in settings.MIDDLEWARES:
            middleware_cls = load_middleware(middlewares_module_class_path)
            self.__app.add_middleware(
                middleware_class=middleware_cls.get_cls(),
                **middleware_cls.get_options_from_settings()
            )

    def __load_plugins(self):
        """
        加载插件
        :return:
        """
        for plugin_module_class_path in settings.PLUGINS:
            plugin_obj = load_module_class_string(plugin_module_class_path)
            if isinstance(plugin_obj, BasePlugin):
                plugin_obj.setup(settings=settings)

    def get_app(self):
        return self.__app


def create_app():
    """
    创建应用
    :return:
    """
    fla = Gesang()
    fla.init_app()
    fla.get_app()
    return fla.get_app()


app = create_app()
