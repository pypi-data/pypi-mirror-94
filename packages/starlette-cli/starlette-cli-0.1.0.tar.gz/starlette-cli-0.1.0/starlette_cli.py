"""
Extensible CLI for Starlette-apps.
"""
import apps
import cli2
import sys
import os

from starlette.routing import Mount


class CliApp(apps.App):
    name = 'cli'

    @property
    def cli(self):
        return cli

    def entry_point(self):
        return cli.entry_point()


cli = cli2.Group(doc=__doc__)
app = CliApp()
project = apps.Project.current()


@app.cli.cmd(color='green')
def middlewares():
    """Dump middlewares for this project."""
    middlewares = project._starlette.user_middleware
    print(f'\nFound {len(middlewares)} middlewares in {project}\n')
    for middleware in middlewares:
        print(''.join([cli2.c.green, middleware.cls.__name__, cli2.c.reset]))
        for key, value in middleware.options.items():
            print(''.join([
                '    ',
                cli2.c.yellow,
                key,
                cli2.c.reset,
                '=',
                cli2.c.red,
                str(value),
                cli2.c.reset
            ]))
        print()


@app.cli.cmd(color='green')
def urls():
    """Dump URLs for this project."""
    def extract_routes(routes, result=None, parents=None):
        result = result if result is not None else dict()
        parents = parents or []
        for route in routes:
            if isinstance(route, Mount):
                extract_routes(route.routes, result, [route] + parents)
            else:
                name = ''
                path = ''
                for parent in reversed(parents):
                    name += parent.name + ':'
                    path += parent.path
                name += route.name
                path += route.path
                result[name] = path
        return result

    data = extract_routes(apps.Project.current()._starlette.routes)
    print(f'\nFound {len(data)} routes in {project}\n')

    if not data:
        return

    minlen = max([len(name) for name in data]) + 1
    for name, path in data.items():
        print(
            cli2.c.green,
            name + ' ' * (minlen - len(name)),
            cli2.c.yellow,
            path,
            cli2.c.reset
        )


@app.cli.cmd
def runserver(*args):
    """
    Web server in development mode.

    ARGS will be passed to uvicorn, example:

        dev --port 777

    As such, this also works to get uvicorn help: dev --help
    """
    modname = sys.argv[0].replace('./', '').replace('.py', '')
    os.execvp(
        'uvicorn',
        ['uvicorn', '--reload'] + [*args] + [modname + ':app'],
    )


@app.cli.cmd(color='green')
def clean():
    """Clean all __pycache__ directories."""
    print('Cleaning __pycache__ directories ...')
    os.execvp('sh', ['sh', '-c', 'find . -name __pycache__ | xargs rm -rf'])
