from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='abel@sky.pro',
            first_name='Aleks',
            last_name='Bel',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('Friday24')
        user.save()
