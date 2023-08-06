import importlib
import pkgutil
from itertools import chain
from types import ModuleType


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

def discover_plugins(*namespaces: ModuleType):
    result = []
    for n in namespaces:
        namespaced_plugins = [
            importlib.import_module(name)
            for finder, name, ispkg
            in iter_namespace(n)
        ]
        result = chain(result, namespaced_plugins)
    return result

def register_plugins(app, plugins):
    for p in plugins:
        sub_app = getattr(p, "app", None)
        sub_app_name = getattr(p, "name", None)
        if sub_app and sub_app_name:
            app.add_typer(sub_app, name=sub_app_name)
