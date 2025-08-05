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
    path('datos_user_admin', views.datos_user_admin, name='datos_user_admin'),
    path('espacio_admin', views.espacio_admin, name='espacio_admin'),
    path('regis_user_admin', views.regis_user_admin, name='regis_user_admin'),
    path('eliminar_user_admin/<int:id>', views.eliminar_user_admin, name='eliminar_user_admin'),
    path('logout', views.logout_view, name='logout'),

    path('editor', views.editor , name='editor'),
    path('espacio_editor', views.espacio_editor , name='espacio_editor'),
    
    path('consultor', views.consultor , name='consultor'),
    path('espacio_con' , views.espacio_con , name='espacio_con'),
    
    
    path('datos_user', views.datos_user, name='datos_user'),
    
    path('perfil_admin', views.perfil_admin, name='perfil_admin'),
    path('cambio_pass', views.cambio_pass, name='cambio_pass')
    

   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]