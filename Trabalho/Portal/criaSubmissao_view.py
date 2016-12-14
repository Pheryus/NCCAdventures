from django.contrib.auth.decorators import login_required
from Portal.forms import SubmissaoForm
from Portal.models import Trabalho, Submissao
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from ldap import ncc

@login_required
def criaSubmissao(request, id):
    usuario = ncc.Ldap().buscaLogin(request.user.username)

    trabalho = Trabalho.objects.filter(id=id)[0]
    submissao = Submissao.objects.filter(trabalhoKey=trabalho, aluno=usuario.uidNumber.value)

    # caso nao exista submissao ainda
    if not submissao:
        if request.method == "POST":
            form = SubmissaoForm(request.POST, request.FILES)
            file = request.POST.get['file']
            if form.is_valid():
                form.save(usuario, trabalho, trabalho.password, file)
                return HttpResponseRedirect(reverse('Portal_criaSubmissao', kwargs={"id": id}))
        else:
            form = SubmissaoForm()

    else:
        if request.method == "POST":

            form = SubmissaoForm(request.POST, request.FILES, instance=submissao[0])

            if form.is_valid():
                form.resave()
                return HttpResponseRedirect(reverse('Portal_criaSubmissao', kwargs={"id": id}))
        else:
            form = SubmissaoForm(instance=submissao[0])

    professor = trabalho.professor
    return render(request, 'Portal/vertrabalho.html', {'professor': professor, 'trabalho': trabalho, "form": form})