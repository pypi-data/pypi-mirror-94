import copy
import importlib
import os
import time
from pathlib import Path
import operator
from gesang.conf import default_settings
from gesang.utils import exc

ENVIRONMENT_VARIABLE = "GESANG_SETTINGS_MODULE"

empty = object()


def new_method_proxy(func):
    def inner(self, *args):
        if self._wrapped is empty:
            self._setup()
        return func(self._wrapped, *args)

    return inner


class LazyObject:
    """
    A wrapper for another class that can be used to delay instantiation of the
    wrapped class.
    By subclassing, you have the opportunity to intercept and alter the
    instantiation. If you don't need to do that, use SimpleLazyObject.
    """

    # Avoid infinite recursion when tracing __init__ (#19456).
    _wrapped = None

    def __init__(self):
        # Note: if a subclass overrides __init__(), it will likely need to
        # override __copy__() and __deepcopy__() as well.
        self._wrapped = empty

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == "_wrapped":
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__["_wrapped"] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == "_wrapped":
            raise TypeError("can't delete _wrapped.")
        if self._wrapped is empty:
            self._setup()
        delattr(self._wrapped, name)

    def _setup(self):
        """
        Must be implemented by subclasses to initialize the wrapped object.
        """
        raise NotImplementedError('subclasses of LazyObject must provide a _setup() method')

    # Because we have messed with __class__ below, we confuse pickle as to what
    # class we are pickling. We're going to have to initialize the wrapped
    # object to successfully pickle it, so we might as well just pickle the
    # wrapped object since they're supposed to act the same way.
    #
    # Unfortunately, if we try to simply act like the wrapped object, the ruse
    # will break down when pickle gets our id(). Thus we end up with pickle
    # thinking, in effect, that we are a distinct object from the wrapped
    # object, but with the same __dict__. This can cause problems (see #25389).
    #
    # So instead, we define our own __reduce__ method and custom unpickler. We
    # pickle the wrapped object as the unpickler's argument, so that pickle
    # will pickle it normally, and then the unpickler simply returns its
    # argument.
    def __reduce__(self):
        if self._wrapped is empty:
            self._setup()
        return (unpickle_lazyobject, (self._wrapped,))

    def __copy__(self):
        if self._wrapped is empty:
            # If uninitialized, copy the wrapper. Use type(self), not
            # self.__class__, because the latter is proxied.
            return type(self)()
        else:
            # If initialized, return a copy of the wrapped object.
            return copy.copy(self._wrapped)

    def __deepcopy__(self, memo):
        if self._wrapped is empty:
            # We have to use type(self), not self.__class__, because the
            # latter is proxied.
            result = type(self)()
            memo[id(self)] = result
            return result
        return copy.deepcopy(self._wrapped, memo)

    __bytes__ = new_method_proxy(bytes)
    __str__ = new_method_proxy(str)
    __bool__ = new_method_proxy(bool)

    # Introspection support
    __dir__ = new_method_proxy(dir)

    # Need to pretend to be the wrapped class, for the sake of objects that
    # care about this (especially in equality tests)
    __class__ = property(new_method_proxy(operator.attrgetter("__class__")))
    __eq__ = new_method_proxy(operator.eq)
    __lt__ = new_method_proxy(operator.lt)
    __gt__ = new_method_proxy(operator.gt)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)

    # List/Tuple/Dictionary methods support
    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)


def unpickle_lazyobject(wrapped):
    """
    Used to unpickle lazy objects. Just return its argument, which will be the
    wrapped object.
    """
    return wrapped


class UserSettingsHolder:
    """Holder for user configured settings."""
    # SETTINGS_MODULE doesn't make much sense in the manually configured
    # (standalone) case.
    SETTINGS_MODULE = None

    def __init__(self, default_settings):
        """
        Requests for configuration variables not in this class are satisfied
        from the module specified in default_settings (if possible).
        """
        self.__dict__['_deleted'] = set()
        self.default_settings = default_settings

    def __getattr__(self, name):
        if not name.isupper() or name in self._deleted:
            raise AttributeError
        return getattr(self.default_settings, name)

    def __setattr__(self, name, value):
        self._deleted.discard(name)
        super().__setattr__(name, value)

    def __delattr__(self, name):
        self._deleted.add(name)
        if hasattr(self, name):
            super().__delattr__(name)

    def __dir__(self):
        return sorted(
            s for s in [*self.__dict__, *dir(self.default_settings)]
            if s not in self._deleted
        )

    def is_overridden(self, setting):
        deleted = (setting in self._deleted)
        set_locally = (setting in self.__dict__)
        set_on_default = getattr(self.default_settings, 'is_overridden', lambda s: False)(setting)
        return deleted or set_locally or set_on_default

    def __repr__(self):
        return '<%(cls)s>' % {
            'cls': self.__class__.__name__,
        }


class LazySettings(LazyObject):
    """
    A lazy proxy for either global Django settings or a custom settings object.
    The user can manually configure settings prior to using them. Otherwise,
    Django uses the settings module pointed to by DJANGO_SETTINGS_MODULE.
    """

    def _setup(self, name=None):
        """
        Load the settings module pointed to by the environment variable. This
        is used the first time settings are needed, if the user hasn't
        configured settings manually.
        """
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            desc = ("setting %s" % name) if name else "settings"
            raise exc.ImproperlyConfigured(
                "Requested %s, but settings are not configured. "
                "You must either define the environment variable %s "
                "or call settings.configure() before accessing settings."
                % (desc, ENVIRONMENT_VARIABLE))

        self._wrapped = Settings(settings_module)

    def __repr__(self):
        # Hardcode the class name as otherwise it yields 'Settings'.
        if self._wrapped is empty:
            return '<LazySettings [Unevaluated]>'
        return '<LazySettings "%(settings_module)s">' % {
            'settings_module': self._wrapped.SETTINGS_MODULE,
        }

    def __getattr__(self, name):
        """Return the value of a setting and cache it in self.__dict__."""
        if self._wrapped is empty:
            self._setup(name)
        val = getattr(self._wrapped, name)

        # Special case some settings which require further modification.
        # This is done here for performance reasons so the modified value is cached.
        if name in {'MEDIA_URL', 'STATIC_URL'} and val is not None:
            val = self._add_script_prefix(val)
        elif name == 'SECRET_KEY' and not val:
            raise exc.ImproperlyConfigured("The SECRET_KEY setting must not be empty.")

        self.__dict__[name] = val
        return val

    def __setattr__(self, name, value):
        """
        Set the value of setting. Clear all cached values if _wrapped changes
        (@override_settings does this) or clear single values when set.
        """
        if name == '_wrapped':
            self.__dict__.clear()
        else:
            self.__dict__.pop(name, None)
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """Delete a setting and clear it from cache if needed."""
        super().__delattr__(name)
        self.__dict__.pop(name, None)

    def configure(self, default_settings=default_settings, **options):
        """
        Called to manually configure the settings. The 'default_settings'
        parameter sets where to retrieve any unspecified values from (its
        argument must support attribute access (__getattr__)).
        """
        if self._wrapped is not empty:
            raise RuntimeError('Settings already configured.')
        holder = UserSettingsHolder(default_settings)
        for name, value in options.items():
            if not name.isupper():
                raise TypeError('Setting %r must be uppercase.' % name)
            setattr(holder, name, value)
        self._wrapped = holder

    @property
    def configured(self):
        """Return True if the settings have already been configured."""
        return self._wrapped is not empty


class Settings:
    def __init__(self, settings_module):
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))

        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module

        mod = importlib.import_module(self.SETTINGS_MODULE)

        tuple_settings = (
            "INSTALLED_APPS",
        )
        self._explicit_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)

                if (setting in tuple_settings and
                        not isinstance(setting_value, (list, tuple))):
                    raise exc.ImproperlyConfigured("The %s setting must be a list or a tuple. " % setting)
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)

        if hasattr(time, 'tzset') and self.TIME_ZONE:
            # When we can, attempt to validate the timezone. If we can't find
            # this file, no check happens and it's harmless.
            zoneinfo_root = Path('/usr/share/zoneinfo')
            zone_info_file = zoneinfo_root.joinpath(*self.TIME_ZONE.split('/'))
            if zoneinfo_root.exists() and not zone_info_file.exists():
                raise ValueError("Incorrect timezone setting: %s" % self.TIME_ZONE)
            # Move the time zone info into os.environ. See ticket #2315 for why
            # we don't do this unconditionally (breaks Windows).
            os.environ['TZ'] = self.TIME_ZONE
            time.tzset()

    def is_overridden(self, setting):
        return setting in self._explicit_settings

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            'cls': self.__class__.__name__,
            'settings_module': self.SETTINGS_MODULE,
        }


settings = LazySettings()
