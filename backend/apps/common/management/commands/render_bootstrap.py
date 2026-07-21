import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run safe one-time Render bootstrap tasks without requiring a Render shell."

    def handle(self, *args, **options):
        self.stdout.write("Running database migrations...")
        call_command("migrate", interactive=False, verbosity=1)

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")

        if username and password:
            User = get_user_model()
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": getattr(User.Role, "ADMINISTRATOR", "administrator"),
                    "is_staff": True,
                    "is_superuser": True,
                },
            )
            user.email = email or user.email
            user.role = getattr(User.Role, "ADMINISTRATOR", "administrator")
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} superuser '{username}'."))
        else:
            self.stdout.write("Skipping superuser setup; admin env vars are not set.")

        if os.getenv("TEQFARM_SEED_DEMO", "false").lower() == "true":
            self.stdout.write("Seeding demo data...")
            call_command("seed_demo")
        else:
            self.stdout.write("Skipping demo seed; TEQFARM_SEED_DEMO is not true.")

        self.stdout.write(self.style.SUCCESS("Render bootstrap complete."))
