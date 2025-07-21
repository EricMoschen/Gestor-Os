import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.views.decorators.http import require_http_methods

from .models import AberturaOS, Cliente, MotivoIntervencao, CentroDeCusto, Colaborador, RegistroInicioOS
from .forms import AberturaOSForm, ClienteForm, MotivoIntervencaoForm, ColaboradorForm


# Tela de Menu
@login_required(login_url='login')
def menuos_view(request):
    return render(request, 'menuos.html')


# Geração automática do número da OS
def gerar_numero_os():
    ano_atual = datetime.now().year
    ano_sufixo = str(ano_atual)[-2:]  # Ex: 2024 -> 24

    os_do_ano = AberturaOS.objects.filter(numero_os__endswith=f"-{ano_sufixo}")
    
    if os_do_ano.exists():
        ultima_os = os_do_ano.order_by('-id').first()
        numero_atual = int(ultima_os.numero_os.split('-')[0])
        novo_numero = numero_atual + 1
    else:
        novo_numero = 1

    numero_formatado = str(novo_numero).zfill(3)  # Ex: 001, 002...
    return f"{numero_formatado}-{ano_sufixo}"


# Criação da OS
@login_required
def criar_os(request):
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
        'motivos': MotivoIntervencao.objects.all()
    })

# Validação AJAX do Centro de Custo
@csrf_exempt
def validar_centrocusto(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        codigo = request.GET.get('centro_de_custo', '').strip()
        if not codigo:
            return JsonResponse({'error': 'Centro de custo não informado'}, status=400)

        valido = CentroDeCusto.objects.filter(codigo_custo=codigo).exists()
        return JsonResponse({'valido': valido})

    return JsonResponse({'error': 'Requisição inválida'}, status=400)


# Página de Sucesso
@login_required
def os_sucesso(request, numero):
    return render(request, 'sucesso.html', {'numero_os': numero})


# Listagem das OSs
@login_required
def listar_os(request):
    ano = request.GET.get('ano')
    prioridade = request.GET.get('prioridade')

    os_list = AberturaOS.objects.all().order_by('-data_abertura')

    if ano:
        os_list = os_list.filter(numero_os__endswith=f"-{ano[-2:]}")

    if prioridade:
        os_list = os_list.filter(prioridade=prioridade)

    anos_disponiveis = sorted(set([os.numero_os[-2:] for os in AberturaOS.objects.all()]), reverse=True)

    return render(request, 'listar-os.html', {
        'os_list': os_list,
        'anos_disponiveis': anos_disponiveis,
        'ano_selecionado': ano,
        'prioridade_selecionada': prioridade,
    })


# Detalhes da OS
@login_required
def detalhes_os(request, numero_os):
    os = get_object_or_404(AberturaOS, numero_os=numero_os)
    return render(request, 'detalhes-os.html', {'os': os})


# Cadastro de Cliente
@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cadastrar_cliente')
    else:
        form = ClienteForm()

    return render(request, 'cadastrar_cliente.html', {'form': form})


# Cadastro de Motivo de Intervenção
@login_required
def cadastrar_motivo(request):
    if request.method == 'POST':
        form = MotivoIntervencaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Motivo de Intervenção cadastrado com sucesso!')
            return redirect('cadastrar_motivo')
    else:
        form = MotivoIntervencaoForm()

    return render(request, 'cadastrar_motivo.html', {'form': form})


# Redirecionamento simples para menuos (caso precise)
def menuos(request):
    return render(request, 'menuos.html')



#iniciar horas nas OS 
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET
from menuos.models import AberturaOS, Colaborador  # importe Colaborador também





@require_GET
def buscar_dados_os(request):
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

    
@require_http_methods(["GET", "POST"])
def iniciar_os_view(request):
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

    return render(request, 'menuos/iniciar_os.html')




from django.shortcuts import render
from .models import RegistroInicioOS, Colaborador, AberturaOS, CentroDeCusto

def relatorio_view(request):
    resultados = []
    tipo = valor = data_inicio = data_fim = None

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        valor = request.POST.get("valor")
        data_inicio = request.POST.get("data_inicio")
        data_fim = request.POST.get("data_fim")

        registros = RegistroInicioOS.objects.all()

        if tipo == "matricula" and valor:
            registros = registros.filter(matricula=valor)
        elif tipo == "os" and valor:
            registros = registros.filter(numero_os=valor)
        elif tipo == "centro_custo" and valor:
            # Ajuste para seu model CentroDeCusto e filtro correto:
            registros = registros.filter(
                numero_os__in=AberturaOS.objects.filter(cc=valor).values_list("numero_os", flat=True)
            )

        if data_inicio and data_fim:
            registros = registros.filter(hora_inicio__date__range=[data_inicio, data_fim])

        resultados = registros.order_by("hora_inicio")

    context = {
        "resultados": resultados,
        "colaboradores": list(Colaborador.objects.values_list("matricula", flat=True)),
        "centros": list(CentroDeCusto.objects.values_list("codigo_custo", flat=True)),
        "ordens": list(AberturaOS.objects.values_list("numero_os", flat=True)),
        "tipo": tipo,
        "valor": valor,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }
    return render(request, "menuos/relatorio.html", context)


#cadastro de Colaboradores
@login_required
def cadastrar_colaborador(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador cadastrado com sucesso!')
            return redirect('cadastrar_colaborador')  # Recarrega a mesma página
    else:
        form = ColaboradorForm()
    
    return render(request, 'cadastrar_colaborador.html', {'form': form})