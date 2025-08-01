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
    path('editar/<int:id_persona>', views.editar, name='editar_persona'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]