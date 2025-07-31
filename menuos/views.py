import json
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required

from .models import (
    AberturaOS, Cliente, MotivoIntervencao, CentroDeCusto, Colaborador, RegistroInicioOS
)
from .forms import (
    AberturaOSForm, ClienteForm, MotivoIntervencaoForm, ColaboradorForm, CentroDeCustoForm
)


# Tela Principal (Menu)
@login_required(login_url='login')
def menuos_view(request):
    """
    Renderiza a página principal do sistema de Ordens de Serviço (Menu).
    Apenas usuários autenticados podem acessar.
    """
    return render(request, 'menuos.html')


#  Geração Automática do Número da Ordem de Serviço (OS)  
def gerar_numero_os():
    """
    Gera um novo número de OS baseado no ano atual e na última OS cadastrada.
    Formato: XXX-AA (ex: 001-24)
    """
    ano_atual = datetime.now().year
    ano_sufixo = str(ano_atual)[-2:]  # Últimos dois dígitos do ano (ex: 2024 -> 24)

    # Busca OS do ano atual
    os_do_ano = AberturaOS.objects.filter(numero_os__endswith=f"-{ano_sufixo}")
    
    if os_do_ano.exists():
        ultima_os = os_do_ano.order_by('-id').first()
        numero_atual = int(ultima_os.numero_os.split('-')[0])
        novo_numero = numero_atual + 1
    else:
        novo_numero = 1

    numero_formatado = str(novo_numero).zfill(3)  # Formata com zeros à esquerda (ex: 001)
    return f"{numero_formatado}-{ano_sufixo}"


# Criação da Ordem de Serviço (OS)

@login_required
@permission_required('menuos.abrir_os', raise_exception=True)
def criar_os(request):
    """
    Cria uma nova OS. 
    No GET, exibe formulário com número de OS gerado automaticamente.
    No POST, salva a OS e redireciona para página de sucesso.
    """
    numero_os = gerar_numero_os()

    if request.method == 'POST':
        form = AberturaOSForm(request.POST)
        if form.is_valid():
            os_obj = form.save(commit=False)
            os_obj.numero_os = numero_os
            os_obj.save()
            return redirect('os_sucesso', numero=os_obj.numero_os)
    else:
        form = AberturaOSForm()

    return render(request, 'abrir_os.html', {
        'form': form,
        'numero_os': numero_os,
        'clientes': Cliente.objects.all(),
        'motivos': MotivoIntervencao.objects.all(),
        'centros': CentroDeCusto.objects.all(),
    })


# Cadastro de Centro de Custo

@login_required
@permission_required('menuos.cadastrar_centro_custo', raise_exception=True)
def cadastrar_centro_de_custo(request):
    """
    View para cadastro de Centros de Custo.
    Exibe o formulário e processa a submissão, retornando mensagens de sucesso ou erro.
    """
    if request.method == 'POST':
        form = CentroDeCustoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Centro de Custo cadastrado com sucesso!')
            return redirect('cadastrar_centro_de_custo')
    else:
        form = CentroDeCustoForm()

    return render(request, 'cadastrar_centro_de_custo.html', {'form': form})

# Página de Sucesso ao Criar OS

@login_required
def os_sucesso(request, numero):
    """
    Exibe página de confirmação de criação de OS, mostrando o número gerado.
    """
    return render(request, 'sucesso.html', {'numero_os': numero})


# Listagem das Ordens de Serviço

@login_required
@permission_required('menuos.listar_os', raise_exception=True)
def listar_os(request):
    ano = request.GET.get('ano')
    prioridade = request.GET.get('prioridade')
    status = request.GET.get('status')
    campo = request.GET.get('campo')
    busca = request.GET.get('busca')

    CAMPO_PERMITIDOS = ['numero_os', 'cc', 'cod_cliente__nome_cliente']

    os_list = AberturaOS.objects.all().order_by('-data_abertura')

    if status:
        os_list = os_list.filter(status=status)
    else:
        os_list = os_list.filter(status='Em Aberto')

    if ano:
        os_list = os_list.filter(numero_os__endswith=f"-{ano[-2:]}")

    if prioridade:
        os_list = os_list.filter(prioridade=prioridade)

    if campo in CAMPO_PERMITIDOS and busca:
        filtro = {f"{campo}__icontains": busca}
        os_list = os_list.filter(**filtro)

    anos_disponiveis = sorted(set([
        os.numero_os[-2:] for os in AberturaOS.objects.all()
    ]), reverse=True)

    return render(request, 'listar-os.html', {
        'os_list': os_list,
        'anos_disponiveis': anos_disponiveis,
        'ano_selecionado': ano,
        'prioridade_selecionada': prioridade,
        'status_selecionado': status,
        'campo_selecionado': campo,
        'busca': busca,
    })


# Detalhes de uma OS

@login_required
def detalhes_os(request, numero_os):
    os = get_object_or_404(AberturaOS, numero_os=numero_os)
    return render(request, 'detalhes-os.html', {'os': os})

# Cadastro de Clientes

@login_required
@permission_required('menuos.cadastrar_cliente', raise_exception=True)
def cadastrar_cliente(request):
    """
    Formulário para cadastro de cliente.
    """
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cadastrar_cliente')
    else:
        form = ClienteForm()

    return render(request, 'cadastrar_cliente.html', {'form': form})


# Cadastro de Motivos de Intervenção

@login_required 
@permission_required('menuos.cadastrar_motivo', raise_exception=True)
def cadastrar_motivo(request):
    """
    Formulário para cadastro de motivos de intervenção.
    """
    if request.method == 'POST':
        form = MotivoIntervencaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Motivo de Intervenção cadastrado com sucesso!')
            return redirect('cadastrar_motivo')
    else:
        form = MotivoIntervencaoForm()

    return render(request, 'cadastrar_motivo.html', {'form': form})


# Busca via AJAX dados da OS e colaborador
@require_GET
def buscar_dados_os(request):
    """
    Busca dados da OS e do colaborador para validação antes de iniciar OS.
    Recebe: numero_os e matricula via GET.
    Retorna JSON com validade e informações básicas.
    """
    numero_os = request.GET.get('numero_os', '').strip()
    matricula = request.GET.get('matricula', '').strip()

    if not numero_os or not matricula:
        return JsonResponse({'valido': False, 'mensagem': 'Campos obrigatórios não preenchidos.'}, status=400)

    try:
        os_obj = AberturaOS.objects.get(numero_os=numero_os)
        colaborador = Colaborador.objects.get(matricula=matricula)

        return JsonResponse({
            'valido': True,
            'descricao_os': os_obj.descricao,
            'nome_colaborador': colaborador.nome
        })
    except (AberturaOS.DoesNotExist, Colaborador.DoesNotExist):
        return JsonResponse({'valido': False})


# Início da OS (registro do início do trabalho)
@login_required
@require_http_methods(["GET", "POST"])
@permission_required('menuos.iniciar_os', raise_exception=True)

def iniciar_os_view(request):
    """
    Tela para iniciar OS e registrar o início do trabalho.
    No GET: exibe formulário.
    No POST (JSON): registra início da OS para o colaborador.
    """
    if request.method == "POST":
        if not request.body:
            return JsonResponse({"sucesso": False, "mensagem": "Dados não enviados."})

        try:
            data = json.loads(request.body)
            matricula = data.get("matricula")
            numero_os = data.get("numero_os")

            colaborador = Colaborador.objects.get(matricula=matricula)
            os = AberturaOS.objects.get(numero_os=numero_os)

            RegistroInicioOS.objects.create(
                matricula=matricula,
                numero_os=numero_os
            )

            return JsonResponse({"sucesso": True})
        except Colaborador.DoesNotExist:
            return JsonResponse({"sucesso": False, "mensagem": "Colaborador não encontrado."})
        except AberturaOS.DoesNotExist:
            return JsonResponse({"sucesso": False, "mensagem": "Ordem de Serviço não encontrada."})
        except Exception as e:
            return JsonResponse({"sucesso": False, "mensagem": str(e)})

    return render(request, 'menuos/lancamento_os.html')


# Cadastro de Colaboradores

@login_required
@permission_required('menuos.cadastrar_colaborador', raise_exception=True)
def cadastrar_colaborador(request):
    """
    Formulário para cadastro de colaboradores.
    """
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador cadastrado com sucesso!')
            return redirect('cadastrar_colaborador')
    else:
        form = ColaboradorForm()
    
    return render(request, 'cadastrar_colaborador.html', {'form': form})


# Lançamento/Apontamento de Ordens de Serviço Pelos Colaboradores
@login_required
@permission_required('menuos.lancar_os', raise_exception=True)
def lancamento_os(request):
    """
    Renderiza a tela para lançamento/início da OS.
    """
    return render(request, 'menuos/lancamento_os.html')


# Listagem das Horas Lançadas/Apontadas Pelos Colaboradores
@login_required
@permission_required('menuos.listar_horas', raise_exception=True)
def listar_horas(request):
    registros = RegistroInicioOS.objects.all().order_by('-hora_inicio')  # ordena do mais recente
    return render(request, 'menuos/listar_horas.html', {'registros': registros})


# Logout do Usuário
@require_GET
def logout_view(request):
    logout(request)
    return HttpResponse("Logout automático feito.")


# Alteração de Status da OS
@require_POST
def alterar_status_os(request, id):
    os_obj = get_object_or_404(AberturaOS, id=id)
    novo_status = request.POST.get('status')
    if novo_status in ['Em Aberto', 'Finalizada']:
        os_obj.status = novo_status
        os_obj.save()
    return redirect('detalhes_os', numero_os=os_obj.numero_os)
