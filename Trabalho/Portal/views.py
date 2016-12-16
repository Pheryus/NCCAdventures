from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from Portal.models import *
from django.core.urlresolvers import reverse
from ldap import ncc
import random
import string

@login_required
def home(request):
	ldap = ncc.Ldap()

	usuario = ldap.buscaLogin(request.user.username)

	if "alunos" not in str(usuario.homeDirectory):
		return homeProfessor(request, usuario)
	else:
		return homeAluno(request, usuario)


def homeAluno(request, usuario):

	trabalhos = []
	flagAluno = True
	#turmas = Turma.objects.filter(alunos__id = str(usuario.uidNumber))
	turmas = Turma.objects.all()
	for i in turmas:
		trabalhos += Trabalho.objects.filter(status = "Em execução", turma = i.id)

	submissao = Submissao.objects.filter(aluno=usuario.uidNumber.value)
	keysubmissao = []
	for i in submissao:
		keysubmissao.append(i.trabalhoKey)

	if request.method == "POST":
		for i in trabalhos:
			if request.POST.get("submit " + str(i.id)):
				if request.POST.get("keycode " + str(i.id), -1) == Trabalho.objects.filter(id=i.id)[0].password:
					return HttpResponseRedirect(reverse("Portal_Submissao",  kwargs = {"id" : i.id } ))
				else:
					return HttpResponseRedirect(reverse('Portal_home'))

	return render(request, 'Portal/home.html', {'usuario': usuario, 'keysubmissao' : keysubmissao, 'trabalhos' : trabalhos, "flagAluno" : flagAluno})

def homeProfessor(request, usuario):
	trabalhos = Trabalho.objects.filter(professor = usuario.uidNumber.value)
	flagAluno = False
	if request.method == "POST":
		for i in trabalhos:
			#mudar estado de algum trabalho

			if not i.removido:
				if request.POST.get(str(i.id)):
					if (i.status == "Não enviado"):
						i.status = "Em execução"
						i.password = geraSenha(6)
					elif (i.status == "Em execução"):
						i.status = "Finalizado"
					i.save()
					return HttpResponseRedirect(reverse('Portal_home'))

				#remover algum trabalho
				elif request.POST.get("remover " + str(i.id)):
					i.removido = True
					i.save()
					return HttpResponseRedirect(reverse('Portal_home'))

	return render(request, 'Portal/home.html', {'usuario': usuario, 'trabalhos' : trabalhos, "flagAluno" : flagAluno })


def geraSenha(n):
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))





