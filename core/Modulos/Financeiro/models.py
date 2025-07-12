from django.db import models
from datetime import datetime

from core.Modulos.Clientes.models import OrdemDeServico

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
    