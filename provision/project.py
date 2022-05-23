from invoke import task

from . import common, django, docker, git, tests


@task
def install_tools(context):
    """Install cli dependencies, and tools needed to install requirements."""
    context.run("pip install setuptools pip pip-tools wheel")


@task
def install_requirements(context):
    """Install local development requirements."""
    envs = [
        "development",
        "base",
    ]
    for env in envs:
        common.success(f"Install requirements with pip from {env}.txt")
        context.run(f"pip install -r requirements/{env}.txt")


@task
def compile(context, update=False):
    """Compile requirements with pip-compile."""
    common.success("Compile requirements with pip-compile")
    upgrade = "-U" if update else ""
    in_files = [
        "requirements/production.in",
        "requirements/development.in",
        "requirements/base.in",
    ]
    for in_file in in_files:
        context.run(f"pip-compile -q {in_file} {upgrade}")


@task
def fill_sample_data(context):
    """Prepare sample data for local usage."""
    django.manage(context, "runscript fill_sample_data")


@task
def init(context):
    """Prepare env for working with project."""
    common.success("Setting up git config")
    git.hooks(context)
    git.gitmessage(context)
    common.success("Initial assembly of all dependencies")
    install_tools(context)
    install_requirements(context)
    docker.build(context)
    django.manage(context, "migrate")
    django.set_default_site(context)
    tests.pytest(context)
    django.createsuperuser(context)
    try:
        fill_sample_data(context)
    except NotImplementedError:
        common.warn(
            "Awesome, almost everything is Done! \n"
            "You're the first developer - pls generate factories \n"
            "for test data and setup development environment",
        )
    context.run("poetry lock --no-update")
