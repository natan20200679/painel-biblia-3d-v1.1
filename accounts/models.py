from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):

    class TipoUsuario(models.TextChoices):
        ALUNO = 'ALUNO', 'Aluno'
        INSTITUICAO = 'INSTITUICAO', 'Instituição'

    tipo = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.ALUNO
    )

    def __str__(self):
        return self.username