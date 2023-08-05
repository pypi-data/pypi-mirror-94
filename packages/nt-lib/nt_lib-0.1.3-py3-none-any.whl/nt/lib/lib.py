import importlib
import pkgutil

import nt
import typer
from nt.lib import command


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

def discover_plugins():
    return [
        importlib.import_module(name)
        for finder, name, ispkg
        in iter_namespace(nt)
        if not name.startswith("nt.lib")
    ]

def register_plugins(app, all_plugins):
    for plugin in all_plugins:
        sub_app = getattr(plugin, "app")
        sub_app_name = getattr(plugin, "name")
        app.add_typer(sub_app, name=sub_app_name)


app = typer.Typer(short_help="This is the lib command")
plugins = discover_plugins() + [command]
register_plugins(app, plugins)

if __name__ == "__main__":
    app()
