from invoke import Exit, UnexpectedExit, task
from . import common, docker

DEFAULT_FOLDERS = "place_collector tasks.py"


@task
def isort(context, path=DEFAULT_FOLDERS, params=""):
    """Command to fix imports formatting."""
    common.success("Linters: ISort running")
    docker.run_container(context, f"isort {path} {params}")


@task
def black(context, path=DEFAULT_FOLDERS):
    """Run `black` linter."""
    common.success("Linters: Black running")
    docker.run_container(context, f"black {path}")


@task
def flake8(context, path=DEFAULT_FOLDERS):
    """Run `flake8` linter."""
    common.success("Linters: Flake8 running")
    docker.run_container(context, f"flake8 {path}")


# pylint: disable=redefined-builtin
@task
def all(context, path=DEFAULT_FOLDERS):
    """Run all linters."""
    common.success("Linters: running all linters")
    linters = (isort, flake8, black)
    failed = []
    for linter in linters:
        try:
            linter(context, path)
        except UnexpectedExit:
            failed.append(linter.__name__)
    if failed:
        common.error(
            f"Linters failed: {', '.join(map(str.capitalize, failed))}",
        )
        raise Exit(code=1)
