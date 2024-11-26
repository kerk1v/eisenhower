from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction

class Command(BaseCommand):
    help = 'Create a superuser and add them to the admins group'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Admin username')
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, help='Admin password')

    def handle(self, *args, **options):
        username = options['username'] or 'admin'
        email = options['email'] or 'admin@example.com'
        password = options['password'] or 'adminpassword'

        with transaction.atomic():
            # Create superuser if doesn't exist
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {username}'))
            else:
                user = User.objects.get(username=username)
                self.stdout.write(self.style.WARNING(f'Superuser {username} already exists'))

            # Add user to admins group
            admins_group = Group.objects.get(name='admins')
            if not user.groups.filter(name='admins').exists():
                user.groups.add(admins_group)
                self.stdout.write(self.style.SUCCESS(f'Added {username} to admins group'))
            else:
                self.stdout.write(self.style.WARNING(f'User {username} is already in admins group'))