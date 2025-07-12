from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

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
