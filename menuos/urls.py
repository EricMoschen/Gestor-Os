from django.urls import path
from . import views

urlpatterns = [
    # Página principal do sistema (menu)
    path('', views.menuos_view, name='menuos'),

    # Rotas relacionadas à abertura e gerenciamento de Ordens de Serviço (OS)
    path('abrir/', views.criar_os, name='abrir_os'),  # Formulário para abrir nova OS
    path('sucesso/<str:numero>/', views.os_sucesso, name='os_sucesso'),  # Página de sucesso após criação de OS

    # Listagem e visualização detalhada de OSs
    path('listar-os/', views.listar_os, name='listar_os'),  # Lista todas as OSs com filtros
    path('detalhes-os/<str:numero_os>/', views.detalhes_os, name='detalhes_os'),  # Detalhes de uma OS específica

    # Rotas para cadastros auxiliares usados no sistema
    path('cadastrar-cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),  # Cadastro de clientes
    path('cadastrar-motivo/', views.cadastrar_motivo, name='cadastrar_motivo'),  # Cadastro de motivos de intervenção
    path('cadastrar-colaborador/', views.cadastrar_colaborador, name='cadastrar_colaborador'),  # Cadastro de colaboradores
    path('cadastrar-centro-custo/', views.cadastrar_centro_de_custo, name='cadastrar_centro_de_custo'),  # Cadastro de centros de custo

    # Rotas para iniciar OS e buscar dados via AJAX
    path('iniciar-os/', views.iniciar_os_view, name='iniciar_os'),  # Tela e API para iniciar o trabalho em uma OS
    path('buscar-dados-os/', views.buscar_dados_os, name='buscar_dados_os'),  # Busca dados via AJAX de OS e colaborador

    # Rotas para lançamentos e visualizações adicionais
    path('lancamento-os/', views.lancamento_os, name='lancamento_os'),  # Tela para lançamento de OS (início do trabalho)
    path('listar-horas/', views.listar_horas, name='listar_horas'),  # Tela para listar horas lançadas pelos colaboradores
    
]
