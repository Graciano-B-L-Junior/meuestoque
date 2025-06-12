# core/models.py
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100, help_text='Nome do produto')
    descricao = models.TextField(blank=True, null=True, help_text='Descrição do produto')
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, help_text='Preço de venda')
    quantidade = models.PositiveIntegerField(default=0, help_text='Quantidade em estoque')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']