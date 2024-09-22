from django.conf import settings
from django.db import models
from django.utils import timezone

class Porteiro(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="Usuário",
        on_delete=models.PROTECT
    )
    
    nome_completo = models.CharField(
        verbose_name="Nome Completo",
        max_length=100
    )
    
    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11
    )
    
    telefone = models.CharField(
        verbose_name="Telefone para Contato",
        max_length=11
    )
    
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento"
    )

    class Meta:
        verbose_name = "Porteiro"
        verbose_name_plural = "Porteiros"
        db_table = "porteiro"

    def __str__(self):
        return self.nome_completo

class Log(models.Model):
    porteiro = models.ForeignKey(
        Porteiro,
        verbose_name="Porteiro",
        on_delete=models.CASCADE
    )
    acao = models.CharField(
        verbose_name="Ação",
        max_length=255
    )
    timestamp = models.DateTimeField(
        verbose_name="Data e Hora",
        default=timezone.now
    )

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        db_table = "log"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.porteiro} - {self.acao} - {self.timestamp}"
