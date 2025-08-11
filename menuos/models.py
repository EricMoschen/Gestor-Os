from django.db import models
from django.utils import timezone
import holidays

class CentroDeCusto(models.Model):
    """
    Modelo que representa os centros de custo da empresa.
    Cada centro de custo possui um código único e uma descrição.
    """
    codigo_custo = models.CharField(max_length=10, unique=True)
    descricao_custo = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.codigo_custo} - {self.descricao_custo}"


class Cliente(models.Model):
    """
    Modelo que representa os clientes cadastrados no sistema.
    Cada cliente tem um código único e um nome.
    """
    codigo_cliente = models.CharField(max_length=20, unique=True)
    nome_cliente = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo_cliente} - {self.nome_cliente}"


class MotivoIntervencao(models.Model):
    """
    Motivos de intervenção possíveis para as Ordens de Serviço.
    Cada motivo tem um código único e uma descrição detalhada.
    """
    codigo_intervencao = models.CharField(max_length=20, unique=True)
    descricao_motivo = models.TextField()

    def __str__(self):
        return f"{self.codigo_intervencao} - {self.descricao_motivo}"


class AberturaOS(models.Model):
    numero_os = models.CharField(max_length=20, unique=True)
    descricao = models.TextField()
    cc = models.CharField("Centro de Custo", max_length=20)

    cod_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cod_intervencao = models.ForeignKey('MotivoIntervencao', on_delete=models.CASCADE)  
    ssm = models.PositiveIntegerField("SSM", null=True, blank=True)

    PRIORIDADES = [
        ('MaquinaParada', 'Máquina Parada'),
        ('OperandoDefeito', 'Operando com Defeito'),
        ('OperandoProgramada', 'Operando Programada'),
        ('OperandoParadaMelhoria', 'Operando Parada Melhoria'),
        ('OperandoMelhoria', 'Operando Melhoria'),
        ('Outros','Outros'),
    ]
    prioridade = models.CharField(max_length=100, choices=PRIORIDADES)

    STATUS_CHOICES = [
        ('Em Aberto', 'Em Aberto'),
        ('Finalizada', 'Finalizada'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Em Aberto')

    data_abertura = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OS {self.numero_os} - Prioridade: {self.get_prioridade_display()} - Status: {self.status}"

class Colaborador(models.Model):
    """
    Representa os colaboradores que podem ser alocados para as OSs.
    Cada colaborador possui matrícula única, nome e função.
    """
    matricula = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    funcao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"



# class RegistroInicioOS(models.Model):
#     """
#     Modelo que registra o início de uma OS por um colaborador.
#     Armazena referência ao colaborador, à OS e horário de início.
#     Também categoriza o dia (normal, sábado, domingo/feriado) automaticamente.
#     """
#     DIA_CHOICES = [
#         ('ND', 'Dia Normal (Seg-Sex)'),
#         ('SA', 'Sábado'),
#         ('DF', 'Domingo ou Feriado'),
#     ]

#     colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
#     abertura_os = models.ForeignKey(AberturaOS, on_delete=models.CASCADE)
#     hora_inicio = models.DateTimeField(default=timezone.now)
#     hora_fim = models.DateTimeField(null=True, blank=True)
#     codigo_dia = models.CharField(max_length=2, choices=DIA_CHOICES, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             ultimo = RegistroInicioOS.objects.filter(
#                 colaborador=self.colaborador,
#                 hora_fim__isnull=True
#             ).order_by('-hora_inicio').first()

#             if ultimo:
#                 ultimo.hora_fim = self.hora_inicio
#                 ultimo.save()

#         data = self.hora_inicio.date()
#         semana = self.hora_inicio.weekday()
#         feriados = holidays.Brazil(years=self.hora_inicio.year)

#         if data in feriados or semana == 6:
#             self.codigo_dia = 'DF'
#         elif semana == 5:
#             self.codigo_dia = 'SA'
#         else:
#             self.codigo_dia = 'ND'

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.colaborador.matricula} - OS {self.abertura_os.numero_os}"



    #  Permissões de acesso
class OrdemServico(models.Model):
    class Meta:
        permissions = [
            ("abrir_os", "Pode abrir nova OS"),
            ("listar_os", "Pode listar OSs"),
            ("cadastrar_cliente", "Pode cadastrar cliente"),
            ("cadastrar_motivo", "Pode cadastrar motivo"),
            ("cadastrar_colaborador", "Pode cadastrar colaborador"),
            ("cadastrar_centro_custo", "Pode cadastrar centro de custos"),   
            ("iniciar_os", "Pode Iniciar OS"),
            ("lancamento_os", "Pode lançar OS"),
            ("listar_horas", "Pode listar horas"),
        ]
