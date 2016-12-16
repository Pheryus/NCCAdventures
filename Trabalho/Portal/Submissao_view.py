from django.contrib.auth.decorators import login_required
from Portal.forms import SubmissaoForm
from Portal.models import Trabalho, Submissao
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from ldap import ncc

@login_required
def TestaSubmissao(request, id):
    usuario = ncc.Ldap().buscaLogin(request.user.username)

    trabalho = Trabalho.objects.filter(id=id)[0]
    submissao = Submissao.objects.filter(trabalhoKey=trabalho, aluno=usuario.uidNumber.value)
    if not submissao:
        return criaSubmissao(request, usuario, trabalho)
    else:
        return modificaSubmissao(request, trabalho, id, submissao)


def criaSubmissao(request, usuario, trabalho):
    if request.method == "POST":
        form = SubmissaoForm(request.POST, request.FILES)
        file = request.POST.get('file')
        if form.is_valid():
            id = form.save(usuario.uidNumber.value, trabalho, trabalho.password, usuario.uid.value)
            return HttpResponseRedirect(reverse('Portal_Submissao', kwargs={"id": id}))
    else:
        form = SubmissaoForm()

    professor = trabalho.professor
    return render(request, 'Portal/criasubmissao.html', {'professor': professor, 'trabalho': trabalho, "form": form})


def modificaSubmissao(request,  trabalho, id, submissao):
    if request.method == "POST":
        form = SubmissaoForm(request.POST, request.FILES, instance=submissao[0])
        if form.is_valid():
            form.resave()
            return HttpResponseRedirect(reverse('Portal_Submissao', kwargs={"id": id}))
    else:
        form = SubmissaoForm(instance=submissao[0])

    professor = trabalho.professor
    return render(request, 'Portal/modificasubmissao.html', {'professor': professor, 'trabalho': trabalho, "form": form})