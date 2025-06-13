# core/forms.py
from django import forms
from .models import Produto, MovimentoEstoque # Importe o novo modelo

# ATUALIZE ESTE FORMULÁRIO
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # REMOVA 'quantidade' desta lista
        fields = ['nome', 'descricao', 'preco_compra', 'preco_venda']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# CRIE ESTE NOVO FORMULÁRIO
class MovimentoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentoEstoque
        fields = ['tipo_movimento', 'quantidade', 'observacao']
        widgets = {
            'tipo_movimento': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }