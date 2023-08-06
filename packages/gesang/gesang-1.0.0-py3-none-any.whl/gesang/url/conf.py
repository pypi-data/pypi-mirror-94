from starlette.applications import Starlette
from gesang.utils.funcs import load_module_class_string
from gesang.conf.settings import settings
import re


def get_allowed_request_methods():
    """
    获取请求允许的方法
    :return:
    """
    if hasattr(settings, "URL_ALLOW_METHODS"):
        allow_methods = getattr(settings, "URL_ALLOW_METHODS")
        if isinstance(allow_methods, (list, tuple)):
            return allow_methods
    return ["GET", "PUT", "DELETE", "POST", "OPTIONS", "HEAD", "TRACE", "CONNECT"]


def _url_join(prefix, url):
    """
    URL拼接

    :param prefix: [str] 前缀
    :param url: [str] 路由
    """
    url_str = f"/{prefix}/{url}/"
    return re.sub(r"/{2,}", "/", url_str)


class Path:
    def __init__(self, url, method, prefix, name):
        self.__url = url
        self.__method = method
        self.__prefix = prefix
        self.__name = name

    @property
    def url(self):
        return self.__url

    @property
    def method(self):
        return self.__method

    @property
    def prefix(self):
        return self.__prefix

    @property
    def name(self):
        return self.__name


def path(url="", method=None, prefix="", name=""):
    """
    路由生成方法

    :param url: [str] 路由地址
    :param method: [callable] 具体方法
    :param prefix: [str] 路由前缀
    :param name: [str] 路由名称
    :return:
    """
    return Path(url=url, method=method, prefix=prefix, name=name)


class UrlManager:

    def __init__(self, top_url_module: str = None, app: Starlette = None):
        self.__top_url_module = top_url_module
        self.__app = None
        if app:
            self.init_app(app=app)

    def init_app(self, app: Starlette):
        """
        初始化app
        :param app: [FastAPI]  fastapi对象
        :return:
        """
        self.__app = app
        url_module_path = settings.CONF_URL
        self.__load_url_module(module_obj_path=url_module_path)

    def __load_url_module(self, module_obj_path, pre_url=None):
        """
        加载路由模块
        :param module_obj_path: [str] 路由模块路径
        :param pre_url: [str] 前置路由
        :return:
        """
        router_obj = load_module_class_string(module_class_string=module_obj_path)
        for router in router_obj:
            if isinstance(router, Path):
                if isinstance(router.method, str):
                    if pre_url:
                        pre_url = _url_join(pre_url, router.url)
                    else:
                        pre_url = router.url
                    self.__load_url_module(module_obj_path=router.method, pre_url=pre_url)
                elif callable(router.method):
                    if pre_url:
                        _url_path = _url_join(pre_url, router.url)
                    else:
                        _url_path = router.url
                    self.__app.add_route(
                        path=_url_path,
                        name=router.name,
                        route=router.method,
                        methods=get_allowed_request_methods()
                    )
