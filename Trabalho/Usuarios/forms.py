# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Usuarios.models import Usuario

class LoginForm(forms.Form):

	username = forms.CharField(label='Nome de usuário',max_length=30)
	password = forms.CharField(label="Senha", max_length=30, widget=forms.PasswordInput)


	def clean_username(self):
		username=self.cleaned_data.get('username')
		
		if not User.objects.filter(username=username):
			raise forms.ValidationError(u'Esse nome de usuário não existe')

		return username

	def clean_password(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if not authenticate(username=username,password=password):
			raise forms.ValidationError(u'Senha incorreta')

		return password

	def save(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		return authenticate(username=username,password=password)


class CreateUserForm(forms.Form):

	username = forms.CharField(label="Nome de usuário", max_length=30)
	password = forms.CharField(label="Senha", max_length=30, widget=forms.PasswordInput)
	email = forms.EmailField(label="Email", max_length=30)
	check = forms.BooleanField(label="Professor?", widget=forms.CheckboxInput, required=False)

	def clean_username(self):
		username = self.cleaned_data.get('username')

		if User.objects.filter(username=username):
			raise forms.ValidationError(u'Esse nome de usuário já existe')

		return username

	def clean_password(self):
		password = self.cleaned_data.get('password')
		return password

	def clean_email(self):
		email = self.cleaned_data.get('email')

		if User.objects.filter(email=email):
			raise forms.ValidationError(u'Esse email já está cadastrado')
		return email

	def save(self):
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		u = User(username=username, email=email)
		u.set_password(password)
		u.save()

		
		if self.cleaned_data.get('check'):
			grau = "Professor"
		else:
			grau = "Estudante"
		user = Usuario(user=u, grau=grau)
		user.save()