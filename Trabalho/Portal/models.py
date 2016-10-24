from __future__ import unicode_literals

from django.db import models
from Usuarios.models import Usuario, Turma

# Create your models here.
class Trabalho(models.Model):
	nome = models.CharField(max_length=30)
	professor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
	descricao = models.CharField(max_length=500)


class Submissao(models.Model):
	nome = models.CharField(max_length=30)
	trabalhoKey = models.ForeignKey(Trabalho)
	trabalho = models.CharField(max_length=500)
