from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from Usuarios.models import Usuario, Turma
from Portal.models import *
from Portal.forms import TrabalhoForm
from django.core.urlresolvers import reverse
from random import *

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
				i.status = "Em execução"
				i.password = geraSenha(6)
				i.save()
				return HttpResponseRedirect(reverse('Portal_home'))

	
	return render(request, 'Portal/home.html', {'usuario': usuario, 'trabalhos' : trabalhos})

def geraSenha(N):
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))



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
def modificaTrabalho(request):

	if request.method == "POST":
		form = TrabalhoForm(request.POST, request.FILES)
	else:
		form = TrabalhoForm()

	return render(request, 'Portal/modificatrabalho.html', {'form' : form})



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

