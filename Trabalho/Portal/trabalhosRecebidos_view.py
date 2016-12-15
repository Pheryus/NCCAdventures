from django.http import Http404
from Portal.models import Trabalho, Submissao
from django.shortcuts import render


def trabalhosRecebidos(request, id):
	trabalho = Trabalho.objects.filter(id=id)
	if trabalho:
		trabalho = trabalho[0]
	else:
		raise Http404
	trabsRecebidos = Submissao.objects.filter(trabalhoKey__id=id)
	return render(request, 'Portal/trabsrecebidos.html', {'trabalho': trabalho, 'trabs' : trabsRecebidos })