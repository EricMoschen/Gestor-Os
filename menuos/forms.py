from django import forms
from .models import AberturaOS, CentroDeCusto, Cliente, MotivoIntervencao, Colaborador


class AberturaOSForm(forms.ModelForm):
    """
    Formulário para criação e edição de Ordens de Serviço (OS).
    Inclui validação customizada para o código do centro de custo.
    """
    class Meta:
        model = AberturaOS
        fields = ['descricao', 'cc', 'cod_cliente', 'cod_intervencao', 'prioridade', 'ssm']
        widgets = {
            'ssm': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Digite o número do SSM',
                'min': 0,
            }),
        }
        
    def clean_cc(self):
        """
        Valida se o código do centro de custo informado existe na base.
        Levanta ValidationError caso o código seja inválido.
        """
        codigo = self.cleaned_data.get('cc')
        if codigo and not CentroDeCusto.objects.filter(codigo_custo=codigo).exists():
            raise forms.ValidationError('Código do centro de custo não encontrado.')
        return codigo


class ClienteForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Clientes.
    Inclui placeholders para facilitar a experiência do usuário.
    """
    class Meta:
        model = Cliente
        fields = ['codigo_cliente', 'nome_cliente']
        widgets = {
            'codigo_cliente': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Código do Cliente',
            }),
            'nome_cliente': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nome do Cliente',
            }),
        }


class MotivoIntervencaoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição dos motivos de intervenção.
    Utiliza widget textarea para descrição longa do motivo.
    """
    class Meta:
        model = MotivoIntervencao
        fields = ['codigo_intervencao', 'descricao_motivo']
        widgets = {
            'codigo_intervencao': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Código da Intervenção',
            }),
            'descricao_motivo': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Descrição do Motivo',
            }),
        }


class CentroDeCustoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Centros de Custo.
    Garante que o código seja único e com tamanho máximo adequado.
    """
    class Meta:
        model = CentroDeCusto
        fields = ['codigo_custo', 'descricao_custo']
        widgets = {
            'codigo_custo': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Código do Centro de Custo (máx. 10 caracteres)'
            }),
            'descricao_custo': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Descrição do Centro de Custo'
            }),
        }



class ColaboradorForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de colaboradores.
    Campos básicos: matrícula, nome e função com placeholders explicativos.
    """
    class Meta:
        model = Colaborador
        fields = ['matricula', 'nome', 'funcao']
        widgets = {
            'matricula': forms.TextInput(attrs={'placeholder': 'Matrícula do colaborador'}),
            'nome': forms.TextInput(attrs={'placeholder': 'Nome do colaborador'}),
            'funcao': forms.TextInput(attrs={'placeholder': 'Função do colaborador'}),
        }