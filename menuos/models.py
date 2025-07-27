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
    tag = models.CharField(max_length=50, blank=True, null=True, help_text="Tag opcional para o centro de custo")
    
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
    cod_intervencao = models.ForeignKey('MotivoIntervencao', on_delete=models.CASCADE)  # ajuste se necessário
    ssm = models.PositiveIntegerField("SSM", null=True, blank=True)

    PRIORIDADES = [
        ('B', 'Baixa'),
        ('A', 'Alta'),
        ('C', 'Crítica'),
    ]
    prioridade = models.CharField(max_length=10, choices=PRIORIDADES)

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



class RegistroInicioOS(models.Model):
    """
    Modelo que registra o início de uma OS por um colaborador.
    Armazena matrícula do colaborador, número da OS e horário de início.
    Também categoriza o dia (normal, sábado, domingo/feriado) automaticamente.
    """
    # Categorias de dias para registro
    DIA_CHOICES = [
        ('ND', 'Dia Normal (Seg-Sex)'),
        ('SA', 'Sábado'),
        ('DF', 'Domingo ou Feriado'),
    ]

    matricula = models.CharField(max_length=20)
    numero_os = models.CharField(max_length=20)
    hora_inicio = models.DateTimeField(default=timezone.now)
    hora_fim = models.DateTimeField(null=True, blank=True)
    codigo_dia = models.CharField(max_length=2, choices=DIA_CHOICES, blank=True)

    def save(self, *args, **kwargs):
        # Atualiza o último lançamento sem hora_fim para este colaborador
        if not self.pk:  # Só faz isso ao criar novo registro
            ultimo = RegistroInicioOS.objects.filter(
                matricula=self.matricula,
                hora_fim__isnull=True
            ).order_by('-hora_inicio').first()

            if ultimo:
                ultimo.hora_fim = self.hora_inicio  # Hora atual usada como fim do anterior
                ultimo.save()

        # Define o código do dia automaticamente
        data = self.hora_inicio.date()
        semana = self.hora_inicio.weekday()  # 0 = segunda, ..., 6 = domingo
        feriados = holidays.Brazil()

        if data in feriados or semana == 6:
            self.codigo_dia = 'DF'  # Domingo ou feriado
        elif semana == 5:
            self.codigo_dia = 'SA'  # Sábado
        else:
            self.codigo_dia = 'ND'  # Dia normal (segunda a sexta, não feriado)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.matricula} - OS {self.numero_os}"