from invoke import task

from . import common, docker


@task
def pytest(context):
    """Run django tests."""
    common.success("Tests running")
    docker.run_container(context, "pytest")
