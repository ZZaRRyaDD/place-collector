from invoke import task

START_COMMAND = "docker-compose -f local.yml"


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
def delcont(context):
    """Delete all docker containers."""
    return context.run("docker rm -f $(docker ps -a -q)")
