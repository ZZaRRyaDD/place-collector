from curses import panel
from invoke import Exit, UnexpectedExit, task
from rich import print, panel

DEFAULT_FOLDERS = "place_collector conftest.py tasks.py"
START_COMMAND = "docker-compose -f local.yml"

def success(msg):
    """Print success message."""
    return print(panel.Panel(msg, style="green bold"))


def warn(msg):
    """Print warning message."""
    return print(panel.Panel(msg, style="yellow bold"))


def error(msg):
    """Print error message."""
    return print(panel.Panel(msg, style="red bold"))


@task
def build(context):
    """Build project."""
    return context.run(f"{START_COMMAND} build")


@task
def run(context):
    """Run postgres, redis, django."""
    return context.run(f"{START_COMMAND} up")


@task
def manage(context, command):
    """Template for python manage.py."""
    return context.run(f"{START_COMMAND} run --rm django python manage.py {command}")


@task
def startapp(context, app_name):
    """Create new app."""
    return context.run(f"{START_COMMAND} run --rm django python manage.py startapp {app_name}")


@task
def isort(context, path=DEFAULT_FOLDERS, params=""):
    """Command to fix imports formatting."""
    success("Linters: ISort running")
    return context.run(f"{START_COMMAND} run --rm django isort {path} {params}")


@task
def flake8(context, path=DEFAULT_FOLDERS):
    """Run `flake8` linter."""
    success("Linters: Flake8 running")
    return context.run(f"{START_COMMAND} run --rm django flake8 {path}")


# pylint: disable=redefined-builtin
@task
def all(context, path=DEFAULT_FOLDERS):
    """Run all linters."""
    success("Linters: running all linters")
    linters = (isort, flake8)
    failed = []
    for linter in linters:
        try:
            linter(context, path)
        except UnexpectedExit:
            failed.append(linter.__name__)
    if failed:
        error(
            f"Linters failed: {', '.join(map(str.capitalize, failed))}",
        )
        raise Exit(code=1)
