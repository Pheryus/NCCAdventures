from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse

from Usuarios.forms import LoginForm, CreateUserForm
from Usuarios.models import Usuario 

@user_passes_test(lambda u: u.is_superuser)	
def create_user(request):

	if request.method == "POST":
		form = CreateUserForm(request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('Usuarios_createuser'))
	else:
		form = CreateUserForm()

	return render(request, 'Usuarios/add_user.html', { 'form' : form })

def login_view(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('Portal_home'))

	if request.method == "POST":
		prox = request.GET.get('prox', '/login/')
		username = request.POST.get('login')
		user = authenticate(username= username, password=request.POST.get('password'))
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('Portal_home'))

	return render(request, 'Usuarios/index.html')


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('Usuarios_index'))