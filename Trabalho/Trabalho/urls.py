"""Trabalho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from Portal import criarTrabalho_view as criaTrab_view, modificaTrabalho_view as modificaTrab_view, \
    trabalhosRecebidos_view, Submissao_view

from Usuarios.views import *
from Portal.views import *
from Turma.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login_view, name="Usuarios_index"),
    url(r'^createuser/$', create_user, name="Usuarios_createuser"),
    url(r'^logout/$', logout_view, name="Usuarios_logout"),
    url(r'^home/$', home, name="Portal_home"),
    url(r'^criatrab/$', criaTrab_view.criaTrabalho, name="Cria_Trab"),
    #url(r'^turma/([0-9]+)/$', turma, name="Portal_turma"),
    url(r'^trabalho/(?P<id>\d+)/$', modificaTrab_view.modificaTrabalho, name="Portal_modificaTrabalho"),
    url(r'^trab/(?P<id>\d+)/$', Submissao_view.TestaSubmissao, name="Portal_Submissao"),
    url(r'^recebidos/([0-9]+)/$', trabalhosRecebidos_view.trabalhosRecebidos, name="Portal_trabalhoRecebidos"),
    #url(r'^files/(?P<trabalho_id>\d+)/$', downloadTrabalho, name="Portal_downloadTrabalho"),
    url(r'^criaturma/$', criaTurma, name="Turma.Cria_Turma")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
