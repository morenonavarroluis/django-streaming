from datetime import datetime
import os
from django.contrib import messages 
import shutil
from django.conf import settings
from django.shortcuts import redirect, render
from .models import Videos , Person , Users ,Rols
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login ,logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db import transaction


# vista del login
def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)  
                
                # Redireccionar según el grupo del usuario
                if user.groups.filter(name='administrador').exists():
                    return redirect('administrador')
                elif user.groups.filter(name='editor').exists():
                    return redirect('editor')
                elif user.groups.filter(name='consultor').exists():
                    return redirect('consultor')
                elif user.groups.filter(name='seguridad').exists():
                    return redirect('datos_user')
                else:
                   
                    return redirect('videos')  
        else:
          
            return render(request, 'paginas/index.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
    
    # Maneja la solicitud GET para mostrar el formulario
    else:
        form = AuthenticationForm()
        return render(request, 'paginas/index.html', {'form': form})

#------------------------------------------------------------#
# vista de la pagina  todos los videos
def videos(request):
    videos = Videos.objects.all()
    return render(request, 'paginas/videos.html', {'videos': videos})
   



def administrador(request):
    video = Videos.objects.all()
    return render(request, 'paginas/admin.html', {'video': video})
    

#funcion para registrar una videos
def video_regis(request):
    if request.method == 'POST':
        video = Videos()       
        video.video_name = request.POST.get('name')
        video.location = request.FILES.get('video')        
        video.save()
        print("Video registrado:", video.video_name)
        return redirect('administrador')  




#funcion para ver los datos de los usuarios    
def datos_user_admin(request):
    groups  = Group.objects.all()
    usuarios = User.objects.all()
    contexto ={
        'usuarios': usuarios , 'groups':  groups
    }
    return render(request, 'paginas/datos_user_admin.html', contexto)


def format_bytes(bytes_value, precision=2):
    """
    Convierte un valor en bytes a una unidad más legible (KB, MB, GB, TB).
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    bytes_value = max(bytes_value, 0)
    pow_val = floor((bytes_value if bytes_value > 0 else 0) / log(1024))
    pow_val = min(pow_val, len(units) - 1)
    bytes_value /= (1 << (10 * pow_val))
    return f"{bytes_value:.{precision}f} {units[pow_val]}"

def espacio_admin(request):
    """
    Vista que calcula el estado del disco y lo pasa al template.
    """
    # Lógica para la primera sección (espacio general)
    try:
        # Usa el directorio raíz de los archivos de medios como punto de referencia
        path_to_check = settings.BASE_DIR 
        
        disk_total_bytes, disk_used_bytes, disk_free_bytes = shutil.disk_usage(path_to_check)
        
        percentage_used = (disk_used_bytes / disk_total_bytes) * 100
        percentage_free = 100 - percentage_used
        
        main_disk_data = {
            'total': format_bytes(disk_total_bytes),
            'used': format_bytes(disk_used_bytes),
            'free': format_bytes(disk_free_bytes),
            'percentage_used': round(percentage_used, 2),
            'percentage_free': round(percentage_free, 2),
            'last_updated': datetime.now().strftime('%H:%M %d/%m/%Y'),
        }
    except Exception as e:
        # Manejo de errores si no se puede acceder a la información del disco
        main_disk_data = None
        print(f"Error al obtener el estado del disco: {e}")

    # Lógica para la segunda sección (particiones del sistema)
    partitions_list = []
    # Usamos una lista de directorios comunes para el ejemplo.
    # Puedes ajustarla según las necesidades de tu servidor.
    partitions_to_check = ['/', '/home', '/var', '/tmp'] 

    for path in partitions_to_check:
        if os.path.exists(path):
            try:
                total, used, free = shutil.disk_usage(path)
                percent = (used / total) * 100
                
                partitions_list.append({
                    'name': path,
                    'total': format_bytes(total),
                    'free': format_bytes(free),
                    'used': format_bytes(used),
                    'percent': round(percent, 2),
                    'bar_class': 'bg-danger' if percent > 90 else ('bg-warning' if percent > 70 else 'bg-success')
                })
            except Exception:
                continue

    context = {
        'main_disk_data': main_disk_data,
        'partitions': partitions_list,
    }

    return render(request, 'paginas/espacio_admin.html', context)


from math import log, floor

def format_bytes(bytes_val, precision=2):
    if bytes_val == 0:
        return '0 B'
    size_name = ('B', 'KB', 'MB', 'GB', 'TB')
    i = int(floor(log(bytes_val, 1024)))
    p = pow(1024, i)
    s = round(bytes_val / p, precision)
    return f"{s} {size_name[i]}"

#funcion para registrar un usuario
def regis_user_admin(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        rol_id = request.POST.get('rol')
        print(rol_id)
        # Validación de campos vacíos
        if not all([first_name, username, password, rol_id]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('datos_user_admin')
        
        # Validación de longitud mínima de password
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('datos_user_admin')
            
        # Validación de formato de username
        if not username.isalnum():
            messages.error(request, 'El nombre de usuario solo puede contener letras y números.')
            return redirect('datos_user_admin')
            
        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'El nombre de usuario ya existe. Por favor, elige otro.')
            return redirect('datos_user_admin')

        try:
        
            with transaction.atomic():
             
                new_user = User.objects.create_user(
                    first_name = first_name,
                    username=username,
                    password=password,
                )

                
                rol_instance = get_object_or_404(Group, id=rol_id)
                new_user.groups.add(rol_instance)

               

                messages.success(request, f'El usuario "{username}" ha sido registrado exitosamente.')
                return redirect('datos_user_admin')
            
        except Exception as e:
            messages.error(request, f'Error inesperado al registrar el usuario: {str(e)}')
            return redirect('datos_user_admin')
    
    
    
    
    return render(request, 'paginas/datos_user_admin.html')

#elimiar una usuario
def eliminar_user_admin(request, id):
     user = User.objects.get(id=id)
     user.delete()
     return redirect('datos_user_admin')
 
 
#logout de la aplicacion
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('index')

#----------------------------------------------------------#


def editor(request):
    video = Videos.objects.all()
   
    return render(request, 'paginas/editor.html', {'video': video})


def espacio_editor(request):
    """
    Vista que calcula el estado del disco y lo pasa al template.
    """
    # Lógica para la primera sección (espacio general)
    try:
        # Usa el directorio raíz de los archivos de medios como punto de referencia
        path_to_check = settings.BASE_DIR 
        
        disk_total_bytes, disk_used_bytes, disk_free_bytes = shutil.disk_usage(path_to_check)
        
        percentage_used = (disk_used_bytes / disk_total_bytes) * 100
        percentage_free = 100 - percentage_used
        
        main_disk_data = {
            'total': format_bytes(disk_total_bytes),
            'used': format_bytes(disk_used_bytes),
            'free': format_bytes(disk_free_bytes),
            'percentage_used': round(percentage_used, 2),
            'percentage_free': round(percentage_free, 2),
            'last_updated': datetime.now().strftime('%H:%M %d/%m/%Y'),
        }
    except Exception as e:
        # Manejo de errores si no se puede acceder a la información del disco
        main_disk_data = None
        print(f"Error al obtener el estado del disco: {e}")

    # Lógica para la segunda sección (particiones del sistema)
    partitions_list = []
    # Usamos una lista de directorios comunes para el ejemplo.
    # Puedes ajustarla según las necesidades de tu servidor.
    partitions_to_check = ['/', '/home', '/var', '/tmp'] 

    for path in partitions_to_check:
        if os.path.exists(path):
            try:
                total, used, free = shutil.disk_usage(path)
                percent = (used / total) * 100
                
                partitions_list.append({
                    'name': path,
                    'total': format_bytes(total),
                    'free': format_bytes(free),
                    'used': format_bytes(used),
                    'percent': round(percent, 2),
                    'bar_class': 'bg-danger' if percent > 90 else ('bg-warning' if percent > 70 else 'bg-success')
                })
            except Exception:
                continue

    context = {
        'main_disk_data': main_disk_data,
        'partitions': partitions_list,
    }

    return render(request, 'paginas/espacio_editor.html', context)



#--------------------------------------------------------------------------------------- #


def consultor(request):
    
      video = Videos.objects.all()
   
      return render(request, 'paginas/consulta.html', {'video': video})
  
def espacio_con(request):
      # Lógica para la primera sección (espacio general)
    try:
        # Usa el directorio raíz de los archivos de medios como punto de referencia
        path_to_check = settings.BASE_DIR 
        
        disk_total_bytes, disk_used_bytes, disk_free_bytes = shutil.disk_usage(path_to_check)
        
        percentage_used = (disk_used_bytes / disk_total_bytes) * 100
        percentage_free = 100 - percentage_used
        
        main_disk_data = {
            'total': format_bytes(disk_total_bytes),
            'used': format_bytes(disk_used_bytes),
            'free': format_bytes(disk_free_bytes),
            'percentage_used': round(percentage_used, 2),
            'percentage_free': round(percentage_free, 2),
            'last_updated': datetime.now().strftime('%H:%M %d/%m/%Y'),
        }
    except Exception as e:
        # Manejo de errores si no se puede acceder a la información del disco
        main_disk_data = None
        print(f"Error al obtener el estado del disco: {e}")

    # Lógica para la segunda sección (particiones del sistema)
    partitions_list = []
    # Usamos una lista de directorios comunes para el ejemplo.
    # Puedes ajustarla según las necesidades de tu servidor.
    partitions_to_check = ['/', '/home', '/var', '/tmp'] 

    for path in partitions_to_check:
        if os.path.exists(path):
            try:
                total, used, free = shutil.disk_usage(path)
                percent = (used / total) * 100
                
                partitions_list.append({
                    'name': path,
                    'total': format_bytes(total),
                    'free': format_bytes(free),
                    'used': format_bytes(used),
                    'percent': round(percent, 2),
                    'bar_class': 'bg-danger' if percent > 90 else ('bg-warning' if percent > 70 else 'bg-success')
                })
            except Exception:
                continue

    context = {
        'main_disk_data': main_disk_data,
        'partitions': partitions_list,
    }

    return render(request, 'paginas/espacio_con.html', context)




def datos_user(request):
    personas = Person.objects.all()
    roles = Rols.objects.all()
    usuarios = User.objects.all()
    return render(request, 'paginas/datos_user.html', {'usuarios': usuarios , 'personas': personas, 'roles': roles})


def perfil_admin(request):
    all_usuario = User.objects.all()
    
    return render(request, 'paginas/perfil_admin.html', {'all_usuario': all_usuario})

def cambio_pass(request):
    if request.method == 'POST':
        
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('perfil_admin') 

        if new_password != confirm_password:
            messages.error(request, 'Las nuevas contraseñas no coinciden.')
            return redirect('perfil_admin')

        if len(new_password) < 8:
            messages.error(request, 'La nueva contraseña debe tener al menos 8 caracteres.')
            return redirect('perfil_admin')

        user.set_password(new_password)
        user.save()
        messages.success(request, 'La contraseña se ha cambiado exitosamente.')
        
        logout(request) 
        return redirect('index')
    
    return render(request, 'paginas/perfil_admin.html')
    