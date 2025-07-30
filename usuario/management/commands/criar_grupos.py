from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from menuos.models import AberturaOS  # Exemplo de model real que usa permissões

class Command(BaseCommand):
    help = 'Cria grupos com permissões específicas'

    def handle(self, *args, **kwargs):
        acessos_admin = Permission.objects.all()

        acessos_pcm = Permission.objects.filter(
            codename__in=[
                'add_aberturaos', 'view_aberturaos', 'change_aberturaos',
                'add_cliente', 'view_cliente',
                'add_motivo', 'view_motivo',
                'add_colaborador', 'view_colaborador',
                'add_centrocusto', 'view_centrocusto',
            ]
        )

        acessos_manut = Permission.objects.filter(
            codename__in=[
                'view_aberturaos', 'add_aberturaos',
            ]
        )

        admin_group, _ = Group.objects.get_or_create(name='Admin')
        pcm_group, _ = Group.objects.get_or_create(name='PCM')
        manut_group, _ = Group.objects.get_or_create(name='Manutenção')

        admin_group.permissions.set(acessos_admin)
        pcm_group.permissions.set(acessos_pcm)
        manut_group.permissions.set(acessos_manut)

        self.stdout.write(self.style.SUCCESS('Grupos criados e permissões atribuídas.'))
