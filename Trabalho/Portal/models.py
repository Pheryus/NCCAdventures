from __future__ import unicode_literals

from django.db import models
from Usuarios.models import Usuario, Turma


def path_diretorio_professor(instance, filename):
	return 'trabalho_{0}/{1}'.format(instance.id, filename)

class Trabalho(models.Model):
	nome = models.CharField(max_length=30)
	professor = models.IntegerField()
	nomeProfessor = models.CharField(max_length=30)
	descricao = models.CharField(max_length=500, blank=True)
	file =  models.FileField(upload_to=path_diretorio_professor, blank=True, null=True)
	status = models.CharField(max_length=30, default="Não enviado")
	password = models.CharField(max_length=8, default="")
	removido = models.BooleanField(default=False)
	turma = models.ForeignKey(Turma, on_delete = models.CASCADE)

	def __str__(self):
		return self.nome

def path_diretorio_aluno(instance, filename):
	return 'trabalho_{0}/{1}/{2}'.format(instance.trabalhoKey.id, instance.aluno, filename)

class Submissao(models.Model):
	nome = models.CharField(max_length=30)
	aluno = models.IntegerField()
	login = models.CharField(max_length=30)
	nomealuno = models.CharField(max_length=30)
	trabalhoKey = models.ForeignKey(Trabalho, on_delete = models.CASCADE)
	trabalho = models.CharField(max_length=500, blank=True)
	file = models.FileField(upload_to=path_diretorio_aluno, blank=True, null=True)
	password = models.CharField(max_length=8, default="")


