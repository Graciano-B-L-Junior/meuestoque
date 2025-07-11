# core/models.py
from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    """
    Representa um produto (peça) no estoque da oficina.
    """
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
        ordering = ['nome'] # Ordena os produtos pelo nome por padrão

    def __str__(self):
        return self.nome

class Movimentacao(models.Model):
    """
    Registra as movimentações de entrada e saída de produtos do estoque.
    """
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
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao'] # Ordena as movimentações da mais recente para a mais antiga

    def __str__(self):
        return f"{self.get_tipo_movimentacao_display()} de {self.quantidade} x {self.produto.nome}"

class Cliente(models.Model):
    """
    Representa um cliente da oficina.
    """
    # Assumindo que 'CLIENTE_DE_USER' indica o usuário que cadastrou ou gerencia esse cliente.
    cliente_de_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='clientes_cadastrados',
        verbose_name="Usuário Responsável"
    )
    nome = models.CharField(max_length=255, verbose_name="Nome")
    sobrenome = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sobrenome")
    celular = models.CharField(max_length=20, verbose_name="Celular")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="E-mail")
    data_cadastro = models.DateTimeField(default=datetime.now, verbose_name="Data de Cadastro")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome', 'sobrenome']

    def __str__(self):
        return f"{self.nome} {self.sobrenome or ''}".strip()

class ItemCliente(models.Model):

    veiculo = models.CharField(null=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class OrdemDeServico(models.Model):
    """
    Representa uma ordem de serviço aberta para um cliente.
    """
    class SituacaoOrdemServico(models.IntegerChoices):
        EM_ANDAMENTO = 1, "Em Andamento"
        AGUARDANDO_PECA = 2, "Aguardando Peça"
        CONCLUIDO = 3, "Concluído"
        CANCELADO = 4, "Cancelado"

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='ordens_de_servico',
        verbose_name="Cliente"
    )
    situacao = models.IntegerField(
        choices=SituacaoOrdemServico.choices,
        default=SituacaoOrdemServico.EM_ANDAMENTO,
        verbose_name="Situação"
    )
    data_inicio = models.DateTimeField(default=datetime.now, verbose_name="Data de Início")
    data_termino = models.DateTimeField(blank=True, null=True, verbose_name="Data de Término")

    item_do_cliente = models.ForeignKey(ItemCliente, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
        ordering = ['-data_inicio']

    def __str__(self):
        return f"OS #{self.pk} - {self.cliente.nome} ({self.get_situacao_display()})"
    
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

class Pagamento(models.Model):
    """
    Registra um pagamento recebido por uma Ordem de Serviço.
    """
    ordem_de_servico = models.ForeignKey(
        OrdemDeServico,
        on_delete=models.CASCADE,
        related_name='pagamentos',
        verbose_name="Ordem de Serviço"
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Pagamento")
    data_pagamento = models.DateTimeField(default=datetime.now, verbose_name="Data do Pagamento")

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-data_pagamento']

    def __str__(self):
        return f"Pagamento de R$ {self.valor} para OS #{self.ordem_de_servico.pk}"