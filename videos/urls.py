from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('', views.videos, name='videos'),
    path('index', views.index, name='index'),
    
    
    path('editar_name_video/<int:video_id>/', views.editar_name_video, name='editar_name_video'),
    path('administrador', views.administrador, name='administrador'),
    path('editar_user_admin/<int:id>', views.editar_user_admin, name='editar_user_admin'),
    path('eliminar_video_admin/<int:video_id>', views.eliminar_video_admin, name='eliminar_video_admin'),
    path('video_regis', views.video_regis, name='video_regis'),
    path('datos_user_admin', views.datos_user_admin, name='datos_user_admin'),
    path('espacio_admin', views.espacio_admin, name='espacio_admin'),
    path('regis_user_admin', views.regis_user_admin, name='regis_user_admin'),
    path('eliminar_user_admin/<int:id>', views.eliminar_user_admin, name='eliminar_user_admin'),
    path('perfil_admin', views.perfil_admin, name='perfil_admin'),
    path('cambio_pass', views.cambio_pass, name='cambio_pass'),
    
    path('logout', views.logout_view, name='logout'),

    path('editor', views.editor , name='editor'),
    path('eliminar_video_editor/<int:video_id>', views.eliminar_video_editor, name='eliminar_video_editor'),
    path('video_editor/<int:video_id>', views.video_editor, name='video_editor'),
    path('regis_editor', views.regis_editor, name='regis_editor'),
    path('perfil_editor', views.perfil_editor, name='perfil_editor'),
    path('cambio_pass_editor', views.cambio_pass_editor, name='cambio_pass_editor'),
    path('espacio_editor', views.espacio_editor , name='espacio_editor'),
    
    path('consultor', views.consultor , name='consultor'),
    path('espacio_con' , views.espacio_con , name='espacio_con'),
    path('perfil_consultor', views.perfil_consultor , name='perfil_consultor'),
    path('cambio_de_password', views.cambio_de_password, name='cambio_de_password'),
    
    path('datos_user', views.datos_user, name='datos_user'),
    path('regis_user_editor', views.regis_user_editor, name='regis_user_editor'),
    path('editar_datos_user/<int:id>', views.editar_datos_user , name='editar_datos_user'),
    path('eliminar_datos_user/<int:id>', views.eliminar_datos_user , name='eliminar_datos_user'),
    path('perfil_segu', views.perfil_segu, name='perfil_segu'),
    path('cambio_password_segu', views.cambio_password_segu , name='cambio_password_segu')
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]