from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('', views.videos, name='videos'),
    path('index', views.index, name='index'),
    path('administrador', views.administrador, name='administrador'),
    path('video_regis', views.video_regis, name='video_regis'),
    path('personas', views.personas, name='personas'),
    path('editar_persona_admin', views.editar_persona_admin, name='editar_persona_admin'),
    path('regis_persona_admin', views.regis_persona_admin, name='regis_persona_admin'),
    path('eliminar_persona/<int:id_persona>', views.eliminar_persona, name='eliminar_persona'),
    path('datos_user_admin', views.datos_user_admin, name='datos_user_admin'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]