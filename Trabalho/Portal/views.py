from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from Usuarios.models import Usuario, Turma
from Portal.models import *
from Portal.forms import TrabalhoForm
from django.core.urlresolvers import reverse
import random
import string

@login_required
def home(request):
	usuario = getUsuario(request)

	if usuario.grau == "Professor":
		return homeProfessor(request, usuario)
	else:
		return homeAluno(request, usuario)


def homeAluno(request, usuario):
	trabalhos = Trabalho.objects.filter(status="Em execução")
	submissao = Submissao.objects.filter(aluno__id=usuario.id)
	if submissao:
		submissao = submissao[0]

	if request.method == "POST":
		for i in trabalhos:
			if request.POST.get("submit " + str(i.id)):
				if request.POST.get("keycode " + str(i.id), -1) == Trabalho.objects.filter(id=i.id)[0].password \
				or submissao:
					return HttpResponseRedirect(reverse("Portal_visualizaTrabalho",  kwargs = {"id" : i.id } ))
				else:
					return HttpResponseRedirect(reverse('Portal_home'))

	return render(request, 'Portal/home.html', {'usuario': usuario, 'trabalhos' : trabalhos, 'submissao' : submissao})

def homeProfessor(request, usuario):
	trabalhos = Trabalho.objects.filter(professor__id=usuario.id)

	if request.method == "POST":
		for i in trabalhos:
			#mudar estado de algum trabalho

			if not i.removido:
				print(request.POST)
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

	return render(request, 'Portal/home.html', {'usuario': usuario, 'trabalhos' : trabalhos})


def geraSenha(n):
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))

@login_required
def criaTrabalho(request):
	usuario = getUsuario(request)
	if usuario.grau != "Professor":
		return Http404

	if request.method == "POST":
		form = TrabalhoForm(request.POST, request.FILES)
		if form.is_valid():
			form.salvandoInstancia(usuario)
			return HttpResponseRedirect(reverse('Cria_Trab'))
	else:
		form = TrabalhoForm()
	return render(request, 'Portal/criatrabalho.html', {'form' : form})


@login_required
def modificaTrabalho(request, id):
	usuario = getUsuario(request)


	"""Checa se é professor"""

	if ehProfessor(usuario):
		trabalhos = Trabalho.objects.filter(professor__id=usuario.id)
		if not autenticacaoProfessor(trabalhos, id):
			raise Http404
	else:
		raise Http404

	trabalho = Trabalho.objects.filter(id=id)
	trabalho = trabalho[0]
	if request.method == "POST":
		form = TrabalhoForm(request.POST,instance=trabalho)
		if form.is_valid():
			form.save(usuario)
			return HttpResponseRedirect(reverse('Portal_home'))
	else:
		form = TrabalhoForm(instance=trabalho)

	return render(request, 'Portal/modificatrabalho.html', {'form' : form })


def trabalhosRecebidos(request, id):
	trabs = Submissao.objects.filter(trabalhoKey__id=id)
	return render(request, 'Portal/trabsrecebidos.html', {'trabs' : trabs})

#Testa se o professor é professor da turma especifica
def autenticacaoProfessor(trabalhos, id):
	for t in trabalhos:
		print(t.id, id)
		if t.id == int(id):
			return True
	return False


def ehProfessor(usuario):
	if usuario.grau != "Professor":
		return False
	return True

def getUsuario(request):
	current_user = request.user
	id_user = current_user.id
	user = Usuario.objects.filter(user_id=id_user)
	return user[0]


def criandoSubmissao(usuario, id, trabalho, password):
	new = Submissao(nome="", password=password, aluno=usuario, trabalhoKey=trabalho, trabalho="")
	new.save()
	return new

def visualizaTrabalho(request, id):
	usuario = getUsuario(request)

	trabalho = Trabalho.objects.filter(id=id)[0]
	submissao = Submissao.objects.filter(trabalhoKey=trabalho, aluno=usuario)
	form = TrabalhoForm(instance=trabalho)
	if not submissao:
		submissao = criandoSubmissao(usuario, id, trabalho, trabalho.password)
	else:
		submissao = submissao[0]

	professor = trabalho.professor
	return render(request, 'Portal/vertrabalho.html', {'professor' : professor, 'trabalho' : trabalho, "submissao" : submissao, "form" : form})

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