"""Module with invoke-commands."""
from invoke import Exit, UnexpectedExit, task
from rich import panel, print

DEFAULT_FOLDERS = "place_collector tasks.py"
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
def run_container(context, command=""):
    """Base template for commands with django container."""
    return context.run(f"{START_COMMAND} run --rm django {command}")


@task
def manage(context, command=""):
    """ase template for commands with python manage.py."""
    run_container(context, f"python manage.py {command}")


@task
def createsuperuser(
    context,
    username="root",
    password="root",
    email="root@root.com",
):
    """Create superuser."""
    manage(
        context,
        f"createsuperuser2 --username {username} --password {password} --noinput --email {email}",
    )


@task
def resetdb(context, apply_migrations=True):
    """Reset database to initial state (including test DB)."""
    success("Reset database to its initial state")
    manage(context, "drop_test_database --noinput")
    manage(context, "reset_db -c --noinput")
    if not apply_migrations:
        return
    manage(context, "makemigrations")
    manage(context, "migrate")
    createsuperuser(context)
    set_default_site(context)


@task
def startapp(context, app_name=""):
    """Create new app."""
    manage(context, f"startapp {app_name}")


@task
def isort(context, path=DEFAULT_FOLDERS, params=""):
    """Command to fix imports formatting."""
    success("Linters: ISort running")
    run_container(context, f"isort {path} {params}")


@task
def black(context, path=DEFAULT_FOLDERS):
    """Run `black` linter."""
    success("Linters: Black running")
    run_container(context, f"black {path}")


@task
def flake8(context, path=DEFAULT_FOLDERS):
    """Run `flake8` linter."""
    success("Linters: Flake8 running")
    run_container(context, f"flake8 {path}")


# pylint: disable=redefined-builtin
@task
def all(context, path=DEFAULT_FOLDERS):
    """Run all linters."""
    success("Linters: running all linters")
    linters = (isort, flake8, black)
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


@task
def install_tools(context):
    """Install cli dependencies, and tools needed to install requirements."""
    context.run("pip install --upgrade setuptools pip pip-tools wheel")


@task
def install_requirements(context, envs=["development", "base"]):
    """Install local development requirements."""
    for env in envs:
        success(f"Install requirements with pip from {env}.txt")
        context.run(
            f"cat requirements/{env}.txt | grep -E '^[^# ]' | cut -d= -f1 | xargs -n 1 poetry add"
        )


@task
def compile(context, update=False):
    """Compile requirements with pip-compile."""
    success("Compile requirements with pip-compile")
    upgrade = "-U" if update else ""
    in_files = [
        "requirements/production.in",
        "requirements/development.in",
        "requirements/base.in",
    ]
    for in_file in in_files:
        context.run(f"pip-compile -q {in_file} {upgrade}")


@task
def pytest(context):
    """Run django tests."""
    success("Tests running")
    run_container(context, "pytest")


def set_default_site(context):
    """Set default site to localhost.

    Set default site domain to `localhost:8000` so `get_absolute_url`
    works correctly in local environment
    """
    manage(
        context,
        "set_default_site --name localhost:8000 --domain localhost:8000",
    )


@task
def pre_push(context):
    """Perform pre push check."""
    success("Perform pre-push check")
    code_style_passed = _run_check(
        context=context,
        checker=all,
        error_msg="Code style checks failed!",
    )
    if not code_style_passed:
        error("Push aborted due to errors\nPLS fix them first!")
        raise Exit(code=1)
    success("Wonderful JOB! Thank You!")


def _run_check(context, checker, error_msg: str, *args, **kwargs):
    try:
        checker(context, *args, **kwargs)
    except (UnexpectedExit, Exit):
        warn(error_msg)
        return False
    return True


@task
def fill_sample_data(context):
    """Prepare sample data for local usage."""
    manage(context, "runscript fill_sample_data")


@task
def pre_push_install(context):
    """Pre-commit install."""
    context.run("pre-commit install")
    context.run("pre-commit run --all-files")


def gitmessage(context):
    """Set default .gitmessage."""
    success("Deploy git commit message template")
    context.run("git config commit.template .gitmessage")


@task
def init(context, clean=False):
    """Prepare env for working with project."""
    success("Setting up git config")
    hooks(context)
    gitmessage(context)
    success("Initial assembly of all dependencies")
    install_tools(context)
    install_requirements(context)
    build(context)
    manage(context, "migrate")
    set_default_site(context)
    pytest(context)
    createsuperuser(context)
    try:
        fill_sample_data(context)
    except NotImplementedError:
        warn(
            "Awesome, almost everything is Done! \n"
            "You're the first developer - pls generate factories \n"
            "for test data and setup development environment",
        )
