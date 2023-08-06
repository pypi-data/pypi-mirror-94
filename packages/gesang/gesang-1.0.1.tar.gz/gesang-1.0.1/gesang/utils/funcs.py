from importlib import import_module
from gesang.utils import exc
from gesang.middleware.base import BaseMiddleware


def load_module_class_string(module_class_string: str, base_cls=None):
    """
    加载模块类

    :param module_class_string: [str] 模块类字符串 "module_path:class_name"
    :param base_cls: [cls] 基类
    :return:
    """
    module_path, cls_name = module_class_string.split(":")
    mod = import_module(module_path)
    if hasattr(mod, cls_name):
        cls = getattr(mod, cls_name)
        if base_cls and type(cls).__name__ == "classobj" and issubclass(cls, base_cls):
            return cls
        else:
            return cls
    else:
        raise exc.ImportModuleClassError(f"Module {module_path} has no attr {cls_name}.")


def load_middleware(module_class_string: str):
    """
    加载中间件类

    :param module_class_string: [str] 模块类字符串 "module_path:class_name"
    :return:
    """
    return load_module_class_string(module_class_string=module_class_string, base_cls=BaseMiddleware)
