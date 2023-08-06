class Error(Exception):
    pass


class ImproperlyConfigured(Error):
    pass


class ImportModuleClassError(Error):
    pass


class ValidatorError(Error):
    pass


class ViewError(Error):
    pass


class MethodNotAllowed(ViewError):
    pass


class DatabaseError(Error):
    pass


class PluginError(Error):
    pass
