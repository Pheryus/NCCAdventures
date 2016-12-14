from django.contrib.auth.decorators import login_required
from Portal.forms import TrabalhoForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from ldap import ncc


def ehProfessor(usuario):
	# testa se é professor
	if "alunos" not in str(usuario.homeDirectory):
		raise Http404

@login_required
def criaTrabalho(request):
	ldap = ncc.Ldap()
	usuario = ldap.buscaLogin(request.user.username)
	ehProfessor(usuario)

	if request.method == "POST":
		form = TrabalhoForm(usuario.uidNumber.value, request.POST, request.FILES)
		if form.is_valid():
			form.salvandoInstancia(usuario.uidNumber.value)
			return HttpResponseRedirect(reverse('Cria_Trab'))
	else:
		form = TrabalhoForm(usuario.uidNumber.value)
	return render(request, 'Portal/criatrabalho.html', {'form' : form})

