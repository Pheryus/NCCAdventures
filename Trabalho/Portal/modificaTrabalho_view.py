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
	if "alunos" in str(usuario.homeDirectory):
		raise Http404

@login_required
def modificaTrabalho(request, id):

	"""Checa se é professor"""
	ldap = ncc.Ldap()
	usuario = ldap.buscaLogin(request.user.username)
	ehProfessor(usuario)
	trabalho = Trabalho.objects.filter(id=id)
	trabalho = trabalho[0]
	msg = ""
	if request.method == "POST":
		msg = request.POST.get("msg")
		form = TrabalhoForm(usuario.uidNumber.value, request.POST, request.FILES, instance=trabalho)
		aux = form
		if form.is_valid() :
			form.modificandoInstancia(instance=trabalho)
			#return render(request, 'Portal/modificatrabalho.html', locals())
			return HttpResponseRedirect(reverse('Portal_modificaTrabalho', kwargs={"id": id}))
		else:
			msg = "Trabalho não está válido"
			return HttpResponseRedirect(reverse('Portal_modificaTrabalho', kwargs={"id": id}))

	else:
		form = TrabalhoForm(usuario.uidNumber.value, instance=trabalho)

	return render(request, 'Portal/modificatrabalho.html', {'form' : form, 'msg' : msg })