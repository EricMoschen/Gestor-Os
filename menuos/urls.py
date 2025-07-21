from django.urls import path
from . import views

urlpatterns = [
    path('', views.menuos_view, name='menuos'),

    # Abertura de OS
    path('abrir/', views.criar_os, name='abrir_os'),
    path('sucesso/<str:numero>/', views.os_sucesso, name='os_sucesso'),

    # Listagem e detalhes
    path('listar-os/', views.listar_os, name='listar_os'),
    path('detalhes-os/<str:numero_os>/', views.detalhes_os, name='detalhes_os'),

    # Cadastros auxiliares
    path('cadastrar-cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('cadastrar-motivo/', views.cadastrar_motivo, name='cadastrar_motivo'),
    path('cadastrar-colaborador/', views.cadastrar_colaborador, name='cadastrar_colaborador'),

    # Validação AJAX
    path('validar-centro-custo/', views.validar_centrocusto, name='validar_centrocusto'),
    
    path('iniciar-os/', views.iniciar_os_view, name='iniciar_os'),
    path('buscar-dados-os/', views.buscar_dados_os, name='buscar_dados_os'),
    
    
    path('relatorio/', views.relatorio_view, name='relatorio'),
]
