import os
import django
from django.core.management import call_command

# Ajuste aqui para o caminho do seu settings.py, ex: 'sistemaos.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from menuos.models import RegistroInicioOS

def main():
    print("Apagando todos os registros do RegistroInicioOS...")
    RegistroInicioOS.objects.all().delete()
    print("Registros apagados.")

    print("Rodando migrações...")
    call_command('migrate')
    print("Migrações aplicadas.")

if __name__ == '__main__':
    main()
