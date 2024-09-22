from django import forms
from .models import Visitante
from django.utils import timezone


class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = [
            'nome_completo', 
            'cpf', 
            'data_nascimento', 
            'numero_casa', 
            'placa_veiculo', 
            'morador_responsavel', 
            'quantidade_visitantes'
        ]

    data_nascimento = forms.DateField(
        label="Data de Nascimento",
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    
    morador_responsavel = forms.CharField(
        label="Morador responsável por autorizar a entrada",
        widget=forms.TextInput(attrs={'placeholder': 'Nome do morador responsável'}),
    )
    
    quantidade_visitantes = forms.IntegerField(
        initial=1,
        label="Quantidade de visitantes",
    )
    
    def save(self, commit=True):
        visitante = super().save(commit=False)
        visitante.horario_chegada = timezone.now()
        if commit:
            visitante.save()
        return visitante



class AutorizaVisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ['morador_responsavel']
        widgets = {
            'morador_responsavel': forms.TextInput(attrs={'placeholder': 'Nome do morador responsável', 'class': 'form-control'}),
        }

    class Meta:
        model = Visitante
        fields = ['morador_responsavel']
