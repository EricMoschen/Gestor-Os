from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Cria os grupos de usuários e atribui permissões'

    def handle(self, *args, **kwargs):
        perms = {
            "abrir_os": Permission.objects.get(codename="abrir_os"),
            "listar_os": Permission.objects.get(codename="listar_os"),
            "cadastrar_cliente": Permission.objects.get(codename="cadastrar_cliente"),
            "cadastrar_motivo": Permission.objects.get(codename="cadastrar_motivo"),
            "cadastrar_colaborador": Permission.objects.get(codename="cadastrar_colaborador"),
            "cadastrar_centro_custo": Permission.objects.get(codename="cadastrar_centro_custo"),
            "lancar_os": Permission.objects.get(codename="lancar_os"),
            "listar_horas": Permission.objects.get(codename="listar_horas"),
        }

        # Admin
        admin, _ = Group.objects.get_or_create(name="Admin")
        admin.permissions.set(perms.values())

        # PCM
        pcm, _ = Group.objects.get_or_create(name="PCM")
        pcm.permissions.set([
            perms["abrir_os"],
            perms["listar_os"],
            perms["cadastrar_cliente"],
            perms["cadastrar_motivo"],
            perms["cadastrar_centro_custo"],
            perms["lancar_os"],
            perms["listar_horas"],
        ])

        # Manutenção
        manutencao, _ = Group.objects.get_or_create(name="Manutenção")
        manutencao.permissions.set([
            perms["listar_os"],
            perms["lancar_os"],
        ])

        self.stdout.write(self.style.SUCCESS("Grupos e permissões criados com sucesso!"))
