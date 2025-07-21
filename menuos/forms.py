from django import forms
from .models import AberturaOS, CentroDeCusto, Cliente, MotivoIntervencao

class AberturaOSForm(forms.ModelForm):
    class Meta:
        model = AberturaOS
        fields = ['descricao', 'cc', 'cod_cliente', 'cod_intervencao', 'prioridade']

    def clean_cc(self):
        codigo = self.cleaned_data.get('cc')
        if codigo and not CentroDeCusto.objects.filter(codigo_custo=codigo).exists():
            raise forms.ValidationError('Código do centro de custo não encontrado.')
        return codigo

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['codigo_cliente', 'nome_cliente']
        widgets = {
            'codigo_cliente': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Código do Cliente'
            }),
            'nome_cliente': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nome do Cliente'
            }),
        }


class MotivoIntervencaoForm(forms.ModelForm):
    class Meta:
        model = MotivoIntervencao
        fields = ['codigo_intervencao', 'descricao_motivo']
        widgets = {
            'codigo_intervencao': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Código da Intervenção'
            }),
            'descricao_motivo': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Descrição do Motivo'
            }),
        }
