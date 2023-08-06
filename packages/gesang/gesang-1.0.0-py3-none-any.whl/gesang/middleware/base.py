class BaseMiddleware:

    middleware_cls = None
    settings_name = None
    default_options = {}

    @classmethod
    def get_cls(cls):
        """
        获取中间件类
        :return:
        """
        return cls.middleware_cls or cls

    @classmethod
    def get_options_from_settings(cls, settings) -> dict:
        """
        从配置信息中，获取中间件参数选项
        :return:
        """
        if hasattr(settings, cls.settings_name):
            options = getattr(settings, cls.settings_name)
            if isinstance(options, dict):
                cls.default_options.update(options)
        return cls.default_options
