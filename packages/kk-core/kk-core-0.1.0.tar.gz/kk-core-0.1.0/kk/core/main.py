import kk
import typer
from kk.core.plugin_utils import discover_plugins, register_plugins

app = typer.Typer(short_help="This is kk-core")
plugins = discover_plugins(kk)
register_plugins(app, plugins)

if __name__ == '__main__':
    app()
