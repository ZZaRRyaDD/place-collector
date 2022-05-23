from invoke import task

from . import common, docker


@task
def manage(context, command=""):
    """ase template for commands with python manage.py."""
    docker.run_container(context, f"python manage.py {command}")


@task
def makemigrations(context, app_name=""):
    """Run makemigrations command and chown created migrations."""
    common.success("Django: Make migrations")
    manage(context, f"makemigrations {app_name}")


@task
def check_new_migrations(context):
    """Check if there is new migrations or not."""
    common.success("Checking migrations")
    manage(context, "makemigrations --check --dry-run")


@task
def migrate(context, app_name=""):
    """Run ``migrate`` command."""
    common.success("Django: Apply migrations")
    manage(context, f"migrate {app_name}")


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
    common.success("Reset database to its initial state")
    manage(context, "drop_test_database --noinput")
    manage(context, "reset_db -c --noinput")
    if not apply_migrations:
        return
    makemigrations(context)
    migrate(context)
    createsuperuser(context)
    set_default_site(context)


@task
def startapp(context, app_name=""):
    """Create new app."""
    manage(context, f"startapp {app_name}")


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
def shell(context, params=""):
    """Shortcut for manage.py shell_plus command.

    Additional params available here:
        https://django-extensions.readthedocs.io/en/latest/shell_plus.html
    """
    common.success("Entering Django Shell")
    manage(context, f"shell_plus --ipython {params}")
