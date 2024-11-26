from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Create default groups and permissions'

    def handle(self, *args, **options):
        # Create groups
        admins_group, created = Group.objects.get_or_create(name='admins')
        users_group, created = Group.objects.get_or_create(name='users')

        # Get content types
        user_content_type = ContentType.objects.get_for_model(User)

        # Get or create permissions
        add_user_perm = Permission.objects.get(
            codename='add_user',
            content_type=user_content_type,
        )
        change_user_perm = Permission.objects.get(
            codename='change_user',
            content_type=user_content_type,
        )
        delete_user_perm = Permission.objects.get(
            codename='delete_user',
            content_type=user_content_type,
        )
        view_user_perm = Permission.objects.get(
            codename='view_user',
            content_type=user_content_type,
        )

        # Assign permissions to admin group
        admins_group.permissions.add(add_user_perm)
        admins_group.permissions.add(change_user_perm)
        admins_group.permissions.add(delete_user_perm)
        admins_group.permissions.add(view_user_perm)

        # Users group only gets view permission
        users_group.permissions.add(view_user_perm)

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))