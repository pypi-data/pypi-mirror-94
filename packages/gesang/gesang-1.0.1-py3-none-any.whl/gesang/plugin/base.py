class BasePlugin:

    def setup(self, settings):
        """
        插件启动入口
        :param settings: [settings] 全局配置对象
        :return:
        """
        raise NotImplemented

    def release(self):
        """
        程序退出调用
        :return:
        """
        raise NotImplemented
