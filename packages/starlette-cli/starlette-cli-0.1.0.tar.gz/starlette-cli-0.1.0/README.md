# Starlette-cli: make your project a cli too!

This is a [starlette-app](https://yourlabs.io/oss/starlette-apps) that provides
a CLI with a few basic Starlette commands, and which your other apps may
extend.

## Example

```python
#!/usr/bin/env python3
import apps

project = apps.Project(
    APPS=['starlette_cli']
)

app = project.starlette(
    routes=[your_route...],
    middleware=[Middleware(your_middleware...)]
)

if __name__ == '__main__':
    project.apps['cli'].entry_point()
```

And your Starlette script becomes an extensible CLI.

### Screenshots

Help & runserver command:

![runserver](https://yourlabs.io/oss/starlette-cli/-/raw/master/example_runserver.png)

Dumping urls and middlewares:

![urls](https://yourlabs.io/oss/starlette-cli/-/raw/master/example_debug.png)

### Install

Install with::

    pip install starlette-cli

### Extend

Add a new command to the CLI with:

```python
from starlette_cli import cli

@cli.cmd
def your_command(...):
    """Your documentation"""
```

Or, from within another starlette-app if you have one:

```python
class YourApp(apps.App):
    def setup(self):
        self.project.apps['cli'].add(your_command)
```
