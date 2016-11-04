# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Portal.models import *

class TrabalhoForm(forms.ModelForm):

	class Meta:
		model = Trabalho
		fields = ['nome', 'turma']
