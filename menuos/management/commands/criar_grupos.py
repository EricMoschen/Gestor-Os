from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from menuos.models import OrdemServico  # ou o modelo onde você definiu as permissões

class Command(BaseCommand):
    help = 'Cria grupos e atribui permissões'

    def handle(self, *args, **kwargs):
        # Criação dos grupos
        grupos = {
            "Admin": ["abrir_os", "listar_os", "cadastrar_cliente", "cadastrar_motivo",
                      "cadastrar_colaborador", "cadastrar_centro_custo", "lancar_os", "listar_horas"],
            "PCM": ["abrir_os", "listar_os", "cadastrar_cliente", "cadastrar_motivo",
                    "cadastrar_colaborador", "cadastrar_centro_custo", "lancar_os", "listar_horas"],
            "Manutencao": ["listar_os", "lancar_os"],
        }

        content_type = ContentType.objects.get_for_model(OrdemServico)

        for grupo_nome, perms_cod in grupos.items():
            grupo, criado = Group.objects.get_or_create(name=grupo_nome)
            grupo.permissions.clear()
            for cod in perms_cod:
                try:
                    perm = Permission.objects.get(codename=cod, content_type=content_type)
                    grupo.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Permissão {cod} não encontrada"))
            grupo.save()
            self.stdout.write(self.style.SUCCESS(f"Grupo '{grupo_nome}' criado/atualizado com permissões."))

