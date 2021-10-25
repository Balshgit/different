from django.core.management.base import BaseCommand
from server.apps.accounts.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not CustomUser.objects.filter(username='admin').exists():
            username = 'admin'
            email = 'admin@admin.ru'
            password = 'admin'
            admin = CustomUser.objects.create_superuser(username=username,
                                                        password=password,
                                                        email=email)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
