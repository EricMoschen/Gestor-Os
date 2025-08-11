import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # ajuste conforme o nome do seu projeto
django.setup()

from menuos.models import AberturaOS, Cliente, MotivoIntervencao
from django.db import transaction

@transaction.atomic
def create_default_os():
    cliente = Cliente.objects.first()
    motivo = MotivoIntervencao.objects.first()
    if not AberturaOS.objects.filter(id=1).exists():
        AberturaOS.objects.create(
            id=1,
            numero_os='DEFAULT-001',
            descricao='Registro default para FK',
            cc='DEFAULT',
            cod_cliente=cliente,
            cod_intervencao=motivo,
            prioridade='Outros',
            status='Em Aberto',
        )

if __name__ == "__main__":
    create_default_os()
