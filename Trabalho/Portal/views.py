from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from Usuarios.models import Usuario, Turma
from Portal.models import *

@login_required
def home(request):
	usuario = getUsuario(request)

	if usuario.grau == "Professor":
		turmas = Turma.objects.filter(professor__id=usuario.id)
		print(turmas)
	else:
		turmas = Turma.objects.filter(alunos__id=usuario.id)
	return render(request, 'Portal/home.html', {'usuario': usuario, 'turmas' : turmas})

def getUsuario(request):
	current_user = request.user
	id_user = current_user.id
	user = Usuario.objects.filter(user_id=id_user)
	return user[0]


@login_required
def turma(request, id):
	usuario = getUsuario(request)
	if usuario.grau == "Professor":
		turmas = Turma.objects.filter(professor__=usuario.id, id=id)
	else:
		turmas = Turma.objects.filter(alunos__id=usuario.id, id=id)
	
	if not turmas:
		raise Http404
	else:
		turma = turmas[0]
	return render(request, 'Portal/turma.html', {'turma' : turma})	
