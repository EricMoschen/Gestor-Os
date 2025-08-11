import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from menuos.models import RegistroInicioOS

RegistroInicioOS.objects.all().delete()

print("Todos os registros de RegistroInicioOS foram apagados.")
