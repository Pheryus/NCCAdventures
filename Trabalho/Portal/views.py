from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from Usuarios.models import Usuario, Turma
from Portal.models import *
from Portal.forms import TrabalhoForm, SubmissaoForm
from django.core.urlresolvers import reverse
from ldap import ncc
import random
import string

@login_required
def home(request):
	ldap = ncc.Ldap()

	usuario = ldap.buscaLogin(request.user.username)

	if "alunos" in str(usuario.homeDirectory):
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

	if request.method == "POST":
		for i in trabalhos:
			if request.POST.get("submit " + str(i.id)):
				if request.POST.get("keycode " + str(i.id), -1) == Trabalho.objects.filter(id=i.id)[0].password:
					return HttpResponseRedirect(reverse("Portal_criaSubmissao",  kwargs = {"id" : i.id } ))
				else:
					return HttpResponseRedirect(reverse('Portal_home'))

	return render(request, 'Portal/home.html', {'usuario': usuario, 'trabalhos' : trabalhos, "flagAluno" : flagAluno})

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


#Testa se o professor é professor da turma especifica
def autenticacaoProfessor(trabalhos, id):
	for t in trabalhos:
		if t.id == int(id):
			return True
	return False


def autenticacaoDownload(request, trabalho_id):
	usuario = ncc.Ldap().buscaLogin(request.user.username)

	#turmas = Turma.objects.filter(alunos__id = usuario.id)
	trabalhos = Trabalho.objects.filter(id = trabalho_id)

	for i in trabalhos:
		for j in turmas:
			if i.turma.id == j.id:
				return True
	return False
 
def downloadTrabalho(request, trabalho_id):

	#if autenticacaoDownload(request, trabalho_id):
	trabalhos = Trabalho.objects.filter(id = trabalho_id)
	if trabalhos:
		trabalho = trabalhos[0]
	else:
		raise Http404

	filename = trabalho.file.name.split('/')[-1]
	arquivo = HttpResponse(trabalho.file, content_type='media/')
	arquivo['Content-Disposition'] = 'attachment; filename=%s' % filename
	return arquivo


@login_required
def turma(request, id):
	usuario = getUsuario(request)
	if usuario.grau == "Professor":
		turmas = Turma.objects.filter(professor__id=usuario.id, id=id)
	else:
		turmas = Turma.objects.filter(alunos__id=usuario.id, id=id)

	if not turmas:
		raise Http404
	else:
		turma = turmas[0]
	return render(request, 'Portal/turma.html', {'turma' : turma})