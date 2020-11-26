
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'medproc'
urlpatterns = [
    path(r'index', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'datapage', views.datapage, name='datapage'),
    path(r'upload', views.model_form_upload, name='upload'),
    path(r'gensympttemp', views.generalsymptview, name='gensymptview'),
    path(r'gendatetemp', views.gendateview, name='gendateview'),
    path(r'gendiagtemp', views.generaldiagview, name='gendiagview'),
    path(r'specsympttemp', views.specsymptview, name='specsymptview'),
    path(r'choosesympt', views.specform, name='choosesympt'),
    path(r'choosediag', views.diagform, name='diagform'),
    path(r'specdiagtemp', views.specdiagview, name='specdiagtemp'),
    path(r'reportselect', views.reportselect, name='reportselect'),
    path(r'altgensymp', views.altgensympt, name='altgensymp'),
path(r'altgendiag', views.altgendiag, name='altgendiag'),
]


# only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

