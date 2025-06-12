# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, help_text='Nome do produto')
    descricao = models.TextField(blank=True, null=True, help_text='Descrição do produto')
    
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2, help_text='Preço de compra',default=0.0)
    
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, help_text='Preço de venda')
    quantidade = models.PositiveIntegerField(default=0, help_text='Quantidade em estoque')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    # Nova propriedade para calcular o lucro
    @property
    def lucro(self):
        if self.preco_venda and self.preco_compra is not None:
            return self.preco_venda - self.preco_compra
        return 0

    # Nova propriedade para calcular a margem de lucro
    @property
    def porcentagem_lucro(self):
        if self.lucro and self.preco_compra and self.preco_compra > 0:
            # Fórmula: (Lucro / Preço de Compra) * 100
            return (self.lucro / self.preco_compra) * 100
        return 0
    
    @property
    def valor_total_estoque(self):
        if self.preco_compra and self.quantidade is not None:
            return self.preco_compra * self.quantidade
        return 0

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']