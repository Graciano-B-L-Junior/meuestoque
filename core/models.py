# core/models.py
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

# ALTERAÇÃO 1: Remova o campo 'quantidade' e adicione a propriedade calculada
class Produto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, help_text='Nome do produto')
    descricao = models.TextField(blank=True, null=True, help_text='Descrição do produto')
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2, help_text='Preço de compra')
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, help_text='Preço de venda')
    # O campo 'quantidade' foi REMOVIDO DAQUI
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    @property
    def quantidade(self):
        """Calcula a quantidade total em estoque somando todas as movimentações."""
        movimentos = self.movimentos.all()
        # Soma as quantidades de entradas e subtrai as de saídas
        total_entradas = movimentos.filter(tipo_movimento='E').aggregate(total=Sum('quantidade'))['total'] or 0
        total_saidas = movimentos.filter(tipo_movimento='S').aggregate(total=Sum('quantidade'))['total'] or 0
        return total_entradas - total_saidas

    # ... (as outras propriedades @property: lucro, porcentagem_lucro, etc. continuam aqui) ...
    # Elas agora usarão a nova propriedade 'quantidade' automaticamente!
    @property
    def lucro(self):
        if self.preco_venda and self.preco_compra is not None:
            return self.preco_venda - self.preco_compra
        return 0

    @property
    def porcentagem_lucro(self):
        if self.lucro and self.preco_compra and self.preco_compra > 0:
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

# ALTERAÇÃO 2: Crie o novo modelo para o histórico
class MovimentoEstoque(models.Model):
    TIPO_MOVIMENTO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='movimentos')
    tipo_movimento = models.CharField(max_length=1, choices=TIPO_MOVIMENTO_CHOICES)
    quantidade = models.PositiveIntegerField()
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_movimento_display()} de {self.quantidade} em {self.produto.nome}"

    class Meta:
        ordering = ['-data_movimentacao']