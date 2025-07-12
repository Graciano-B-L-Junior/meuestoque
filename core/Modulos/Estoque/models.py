
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from core.Modulos.Clientes.models import OrdemDeServico

class Produto(models.Model):
    estoque_usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='produtos_cadastrados',
        verbose_name="Usuário do Estoque",
        null=True
    )
    nome = models.CharField(max_length=255, verbose_name="Nome do Produto")
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço de Custo", null=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço de Venda", null=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Movimentacao(models.Model):

    class TipoMovimentacao(models.IntegerChoices):
        ENTRADA = 1, "Entrada"
        SAIDA = 2, "Saída"

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='movimentacoes',
        verbose_name="Produto"
    )
    quantidade = models.IntegerField(verbose_name="Quantidade")
    tipo_movimentacao = models.IntegerField(
        choices=TipoMovimentacao.choices,
        verbose_name="Tipo de Movimentação"
    )
    descricao = models.CharField(max_length=500, blank=True, null=True, verbose_name="Descrição")
    data_movimentacao = models.DateTimeField(default=datetime.now, verbose_name="Data da Movimentação")

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        ordering = ['-data_movimentacao']

    def __str__(self):
        return f"{self.produto.nome} - {self.get_tipo_movimentacao_display()}"

class ProdutoOrdemServico(models.Model):
    """
    Tabela intermediária para representar um produto específico utilizado em uma Ordem de Serviço.
    Isso permite adicionar atributos como 'quantidade_usada' ou 'preco_venda_na_os' se necessário.
    No seu diagrama, `ESTOQUE: FK(MOVIMENTACAO)` em Produto_OS é peculiar.
    Se a intenção é linkar diretamente a movimentação de baixa que ocorreu para este produto na OS,
    então 'movimentacao' seria uma FK aqui.
    Para o propósito de um MVP e o uso comum, vou linkar ao Produto e à OS.
    Se 'ESTOQUE' no diagrama se refere à tabela 'Produto', então seria FK(Produto).
    Se se refere à 'Movimentacao' específica que deu baixa, seria FK(Movimentacao).
    Considerando o uso prático, vincular ao Produto é mais comum para listar os itens da OS.
    Se precisar vincular à movimentação exata de baixa, adicione o campo 'movimentacao' ForeignKey.
    """
    ordem_de_servico = models.ForeignKey(
        OrdemDeServico,
        on_delete=models.CASCADE,
        related_name='itens_os',
        verbose_name="Ordem de Serviço"
    )
    movimentacao = models.ForeignKey(
        Movimentacao,
        on_delete=models.CASCADE,
        related_name='usos_em_os',
        verbose_name="Produto em Movimentação"
    )

    class Meta:
        verbose_name = "Produto na OS"
        verbose_name_plural = "Produtos na OS"

    def __str__(self):
        return f"Orden de servico de {self.ordem_de_servico.cliente.nome}"
