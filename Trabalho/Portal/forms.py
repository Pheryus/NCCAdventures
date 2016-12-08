# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Portal.models import *

class TrabalhoForm(forms.ModelForm):

	descricao = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}), required=False)
	class Meta:
		model = Trabalho
		fields = ['nome', 'file', 'descricao']


	def clean(self):
		if not (self.cleaned_data.get('file') or self.cleaned_data.get('descricao')):
			raise forms.ValidationError('É necessário ter um arquivo ou descrição')


	def salvandoInstancia(self, professor):
		trabalho = Trabalho(nome=self.cleaned_data.get('nome'),
			descricao=self.cleaned_data.get('descricao'),
			file=self.cleaned_data.get('file'),
			professor=professor
			)
		trabalho.save()

