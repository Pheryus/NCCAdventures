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
		trabalhos = Trabalho.objects.filter(professor__id=usuario.id)
	else:
		trabalhos = []

	if request.method == "POST":
		for i in trabalhos:
			if request.POST.get(str(i.id)):
				if (i.status == "Não enviado"):
					i.status = "Em execução"
					i.password = geraSenha(6)
				elif (i.status == "Em execução"):
					i.status = "Finalizado"
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
	print(usuario.id)
	if request.method == "POST":
		form = TrabalhoForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(usuario)
			return HttpResponseRedirect(reverse('Cria_Trab'))
	else:
		form = TrabalhoForm()
	return render(request, 'Portal/criatrabalho.html', {'form' : form})


@login_required
def modificaTrabalho(request, id):
	usuario = getUsuario(request)

	if ehProfessor(usuario):
		trabalhos = Trabalho.objects.filter(professor__id=usuario.id)
		if not autenticacaoProfessor(trabalhos, id):
			raise Http404

	else:
		raise Http404


	if request.method == "POST":
		form = TrabalhoForm(request.POST, request.FILES)
	else:
		form = TrabalhoForm()

	return render(request, 'Portal/modificatrabalho.html')



#Testa se o professor é professor da turma especifica
def autenticacaoProfessor(trabalhos, id):

	for t in trabalhos:
		if t.id == id:
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

