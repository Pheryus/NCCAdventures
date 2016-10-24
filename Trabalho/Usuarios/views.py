from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from Usuarios.forms import LoginForm, CreateUserForm
from Usuarios.models import Usuario 


def create_user(request):

	if request.method == "POST":
		form = CreateUserForm(request.POST)

		if form.is_valid():
			form.save()
			
	else:
		form = CreateUserForm()

	return render(request, 'Usuarios/add_user.html', { 'form' : form })

def login_view(request):
	prox = request.GET.get('prox', '/login/')
	if request.method == "POST":
		form = LoginForm(request.POST)

		if form.is_valid():
			user = form.save()			
			login(request, user)
			return HttpResponseRedirect(prox)
	else:
		form = LoginForm()

	return render(request, 'Usuarios/index.html', { 'form' : form, 'prox':prox})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('Usuarios_index'))