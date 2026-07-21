import os

from django.core.management import call_command


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")


def main():
    call_command("render_bootstrap")

    port = os.getenv("PORT", "8000")
    os.execvp(
        "gunicorn",
        [
            "gunicorn",
            "config.wsgi:application",
            "--bind",
            f"0.0.0.0:{port}",
        ],
    )


if __name__ == "__main__":
    main()
