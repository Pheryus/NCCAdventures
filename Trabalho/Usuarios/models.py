from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
	user = models.OneToOneField(User, related_name='user_profile')
	grau = models.CharField(max_length=30)

	def __unicode__(self):
		return "%s %s" % (self.user.username, self.grau)


class Turma(models.Model):
	nome = models.CharField(max_length=30)
	professor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	alunos = models.ManyToManyField(Usuario, related_name="Estudantes")

	def __unicode__(self):
		return "%s %s" % (self.nome, self.professor)