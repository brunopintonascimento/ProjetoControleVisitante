from django.db import models
from django.utils import timezone

class Visitante(models.Model):
    registrado_por = models.ForeignKey(
        "porteiros.Porteiro",
        verbose_name="Porteiro responsável pelo registro",
        on_delete=models.PROTECT,
    )
    
    nome_completo = models.CharField(
        verbose_name="Nome Completo",
        max_length=150,
    )
    
    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11,
    )

    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento",
    )

    numero_casa = models.PositiveSmallIntegerField(
        verbose_name="Número da casa a ser visitada",
    )

    placa_veiculo = models.CharField(
        verbose_name="Placa do Veículo",
        max_length=7,
        blank=True,
        null=True,
    )

    horario_chegada = models.DateTimeField(
        verbose_name="Horário de Chegada na Portaria",
        auto_now_add=True,  # Define automaticamente a data/hora de criação
    )

    horario_saida = models.DateTimeField(
        verbose_name="Horário de saída do condomínio",
        blank=True,
        null=True,
    )

    horario_autorizacao = models.DateTimeField(
        verbose_name="Horário de Autorização de Entrada",
        blank=True,
        null=True,
    )

    morador_responsavel = models.CharField(
        verbose_name="Nome do morador responsável por autorizar a entrada",
        max_length=50,
        blank=True,
    )

    quantidade_visitantes = models.PositiveIntegerField(
        verbose_name="Quantidade de visitantes",
        default=1,
    )

    # Adicionando o campo 'status'
    STATUS_VISITANTE = [
        ("AGUARDANDO", "Aguardando autorização"),
        ("EM_VISITA", "Em visita"),
        ("FINALIZADO", "Visita finalizada"),
    ]
    status = models.CharField(
        verbose_name="Status",
        max_length=10,
        choices=STATUS_VISITANTE,
        default="AGUARDANDO",
    )

    # Métodos para autorizar e finalizar visitas
    def autorizar_visita(self):
        """Define o horário de autorização quando a visita é autorizada"""
        if self.status == "EM_VISITA" and not self.horario_autorizacao:
            self.horario_autorizacao = timezone.now()
            self.save()

    def finalizar_visita(self):
        """Define o horário de finalização e saída quando o status é 'FINALIZADO'"""
        if self.status == "FINALIZADO":
            if not self.horario_saida:
                self.horario_saida = timezone.now()  # Define horário de saída
            self.save()

    class Meta:
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"
        db_table = "visitante"

    def __str__(self):
        return self.nome_completo
