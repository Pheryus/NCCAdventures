from ldap import ncc
from Portal.models import Trabalho
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse


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
    # if autenticacaoDownload(request, trabalho_id):
    trabalhos = Trabalho.objects.filter(id=trabalho_id)
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



def ehProfessor(request):


