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
# vista del login
def index(request):
      if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's built-in authenticate function
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user exists and the password is correct, log them in
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            # Redirect to a success page
            return redirect('administrador')
        else:
            # If authentication fails, display an error message
            messages.error(request, "Invalid username or password.")
            
    
    
    
      return render(request, 'paginas/index.html', {'error': 'Credenciales incorrectas'})
         
   


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

 #funcion para ver los detalles de personas
def personas(request):
    person = Person.objects.all()
    return render(request, 'paginas/personas.html', {'person': person})

#funcion para editar una persona
def editar_persona_admin(request):
    if request.method == 'POST':
        id_persona = request.POST.get('id_persona')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        cargo = request.POST.get('cargo')
        gerencia = request.POST.get('gerencia')
        
        persona = Person.objects.get(id_persona=id_persona)
        persona.nombre = nombre
        persona.apellido = apellido
        persona.cedula = cedula
        persona.cargo =  cargo
        persona.gerencia = gerencia
        persona.save()
        
        return redirect('personas')  

#funcion para registrar una persona
def regis_persona_admin(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        cargo = request.POST.get('cargo')
        gerencia = request.POST.get('gerencia')
        
        persona = Person()
        persona.nombre = nombre
        persona.apellido = apellido
        persona.cedula = cedula
        persona.cargo = cargo
        persona.gerencia = gerencia
        persona.save()
        
        return redirect('personas')
    
#elimiar una persona 
def eliminar_persona(request, id_persona):
     persona = Person.objects.get(id_persona=id_persona)
     persona.delete()
     return redirect('personas')

#funcion para ver los datos de los usuarios    
def datos_user_admin(request):
    personas = Person.objects.all()
    roles = Rols.objects.all()
    usuarios = Users.objects.all()
    return render(request, 'paginas/datos_user_admin.html', {'usuarios': usuarios , 'personas': personas, 'roles': roles})


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
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        rol_id = request.POST.get('rol')
        persona_id = request.POST.get('persona')
        
        # Validación de campos vacíos
        if not all([username, password, rol_id, persona_id]):
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
        if Users.objects.filter(username__iexact=username).exists():
            messages.error(request, 'El nombre de usuario ya existe. Por favor, elige otro.')
            return redirect('datos_user_admin')
            
        try:
            # Obtener la instancia del rol y la persona
            rol_instance = get_object_or_404(Rols, id_rol=rol_id)
            persona_instance = get_object_or_404(Person, id_persona=persona_id)

            # Crear usuario con contraseña encriptada
            new_user = Users(
                username=username,
                password=make_password(password),  # Encriptación segura
                rol_id=rol_instance,  # Asignar la instancia del rol
                person_id=persona_instance  # Asignar la instancia de la persona
            )
            new_user.save()
            messages.success(request, f'El usuario "{username}" ha sido registrado exitosamente como administrador.')
            return redirect('datos_user_admin')
            
        except Exception as e:
            messages.error(request, f'Error inesperado al registrar el usuario: {str(e)}')
            return redirect('datos_user_admin')
    
    # Si el método no es POST, renderizar el template
    context = {
        'roles': Rols.objects.all(),  # Asegúrate de que tienes un modelo Rols
        'personas': Person.objects.all()  # Asegúrate de que tienes un modelo Person
    }
    return render(request, 'paginas/datos_user_admin.html', context)

#elimiar una persona 
def eliminar_user_admin(request, id):
     user = Users.objects.get(id=id)
     user.delete()
     return redirect('datos_user_admin')
 
 
#logout de la aplicacion
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('index')