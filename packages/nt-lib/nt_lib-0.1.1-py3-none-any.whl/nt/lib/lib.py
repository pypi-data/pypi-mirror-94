import importlib
import pkgutil

import nt
import typer
from nt.lib import command

app = typer.Typer(help="This is nt-app.app's app!")
app.add_typer(command.app, name="subcommand")

def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in iter_namespace(nt)
    if not name.startswith("nt.lib")
}

print(discovered_plugins)
for v in discovered_plugins.values():
    sub_app = getattr(v, "app")
    app.add_typer(sub_app)

if __name__ == "__main__":
    app()
