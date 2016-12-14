from django.contrib.auth.decorators import login_required
from Portal.forms import TrabalhoForm
from Portal.models import Trabalho
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
def modificaTrabalho(request, id):

	"""Checa se é professor"""
	ldap = ncc.Ldap()
	usuario = ldap.buscaLogin(request.user.username)
	ehProfessor(usuario)

	trabalho = Trabalho.objects.filter(id=id)
	trabalho = trabalho[0]
	print(trabalho)
	if request.method == "POST":
		form = TrabalhoForm(usuario.uidNumber.value, request.POST, instance=trabalho)
		if form.is_valid():
			form.save(usuario)
			return HttpResponseRedirect(reverse('Portal_home'))
	else:
		form = TrabalhoForm(usuario.uidNumber.value, instance=trabalho)

	return render(request, 'Portal/modificatrabalho.html', {'form' : form })