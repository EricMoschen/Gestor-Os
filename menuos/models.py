from django.db import models
from django.utils import timezone
import holidays

class CentroDeCusto(models.Model):
    codigo_custo = models.CharField(max_length=10, unique=True)
    descricao_custo = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo_custo} - {self.descricao_custo}"


class Cliente(models.Model):
    codigo_cliente = models.CharField(max_length=20, unique=True)
    nome_cliente = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo_cliente} - {self.nome_cliente}"


class MotivoIntervencao(models.Model):
    codigo_intervencao = models.CharField(max_length=20, unique=True)
    descricao_motivo = models.TextField()

    def __str__(self):
        return f"{self.codigo_intervencao} - {self.descricao_motivo}"


class AberturaOS(models.Model):
    numero_os = models.CharField(max_length=20, unique=True)
    descricao = models.TextField()
    cc = models.CharField("Centro de Custo", max_length=20)

    cod_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cod_intervencao = models.ForeignKey(MotivoIntervencao, on_delete=models.CASCADE)

    PRIORIDADES = [
        ('B', 'Baixa'),
        ('A', 'Alta'),
        ('C', 'Crítica'),
    ]
    prioridade = models.CharField(max_length=10, choices=PRIORIDADES)
    data_abertura = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OS {self.numero_os} - Prioridade: {self.get_prioridade_display()}"




class Colaborador(models.Model):
    matricula = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    funcao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"




class RegistroInicioOS(models.Model):
    DIA_CHOICES = [
        ('ND', 'Dia Normal (Seg-Sex)'),
        ('SA', 'Sábado'),
        ('DF', 'Domingo ou Feriado'),
    ]

    matricula = models.CharField(max_length=20)
    numero_os = models.CharField(max_length=20)
    hora_inicio = models.DateTimeField(default=timezone.now)
    codigo_dia = models.CharField(max_length=2, choices=DIA_CHOICES, blank=True)

    def save(self, *args, **kwargs):
        data = self.hora_inicio.date()
        semana = self.hora_inicio.weekday()  # 0 = segunda, 6 = domingo
        feriados = holidays.Brazil()

        if data in feriados or semana == 6:
            self.codigo_dia = 'DF'
        elif semana == 5:
            self.codigo_dia = 'SA'
        else:
            self.codigo_dia = 'ND'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.matricula} - OS {self.numero_os}"
