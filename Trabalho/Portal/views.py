from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Usuarios.models import Usuario, Turma
from Portal.models import *

@login_required
def home(request):
	current_user = request.user
	id_user = current_user.id
	user = Usuario.objects.filter(user_id=id_user)
	user = user[0]
	if user.grau == "Professor":
		turmas = Turma.objects.filter(professor=user.id)
	else:
		turmas = Turma.objects.filter(alunos=user.id)
	return render(request, 'Portal/home.html')