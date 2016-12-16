# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Portal.models import *

class TrabalhoForm(forms.ModelForm):

	descricao = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}), required=False)
	class Meta:
		model = Trabalho
		fields = ['nome', 'file', 'descricao', 'turma']


	def __init__(self, idProfessor, *args, **kwargs):
		super (TrabalhoForm, self).__init__(*args, **kwargs)
		self.fields['turma'].queryset = Turma.objects.filter(professor = idProfessor)


	def clean(self):
		if not (self.cleaned_data.get('file') or self.cleaned_data.get('descricao')):
			raise forms.ValidationError('É necessário ter um arquivo ou descrição')

	def salvandoInstancia(self, professor, nome):
		trabalho = Trabalho(nome=self.cleaned_data.get('nome'),
			descricao=self.cleaned_data.get('descricao'),
			professor=professor,
			nomeProfessor=nome,
			turma=self.cleaned_data.get('turma')
			)
		trabalho.save()
		trabalho.file=self.cleaned_data.get('file')
		trabalho.save()
		return trabalho.id

	def modificandoInstancia(self, instance):
		data = self.cleaned_data
		instance.descricao = data['descricao']
		instance.nome = data['nome']
		instance.file = data['file']
		instance.save()


	def getFile(self):
		return self.cleaned_data['file']

class SubmissaoForm(forms.ModelForm):

	class Meta:
		model = Submissao
		fields = ['nome', 'file', 'trabalho']


	def clean(self):
		if not (self.cleaned_data.get('file') or self.cleaned_data.get('trabalho')):
			raise forms.ValidationError('É necessário enviar pelo menos uma descrição textual ou um arquivo com o trabalho!')


	def save(self, alunoid, trabalhoid, password, login):
		data = self.cleaned_data

		submissao = Submissao(nome=data['nome'], file=data['file'], trabalho=data['trabalho'], \
			aluno=alunoid, login=login, trabalhoKey=trabalhoid, password=password)
		submissao.save()
		return submissao.id

	def resave(self):
		data = self.cleaned_data
		self.instance.nome = data['nome']
		self.instance.file = data['file']
		self.instance.trabalho = data['trabalho']
		self.instance.save()

