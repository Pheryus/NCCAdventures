from django.shortcuts import render
from ldap import ncc
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from Usuarios.models import Turma

def criaTurma(request):
    ldap = ncc.Ldap()
    professor = []
    alunos = []
    for i in ldap.listaUsuarios():
        if "aluno" in str(i.homeDirectory):
            alunos.append(i)
        else:
            professor.append(i)

    turmas = Turma.objects.all()
    if request.method == "POST":
        idProfessor = request.POST.get("org_list")
        nomeTurma = request.POST.get("nomeMateria")
        novaTurma = Turma(professor = idProfessor, nome=nomeTurma)
        novaTurma.save()

        return HttpResponseRedirect(reverse('Turma.Cria_Turma'))

    return render (request, 'Turma/cria_turma.html', {'professor' : professor, 'alunos' : alunos, 'turmas' : turmas } )

