from django.contrib import admin
from .models import AberturaOS, Cliente, MotivoIntervencao, CentroDeCusto, Colaborador, RegistroInicioOS, OrdemServico
# Register your models here.
admin.site.register(AberturaOS)
admin.site.register(Cliente)
admin.site.register(MotivoIntervencao)
admin.site.register(CentroDeCusto)
admin.site.register(Colaborador)
admin.site.register(RegistroInicioOS)
admin.site.register(OrdemServico)
