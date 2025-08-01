from django.shortcuts import redirect, render
from .models import Videos , Person
from django.shortcuts import get_object_or_404

# vista del login
def index(request):
    return render(request, 'paginas/index.html')

# vista de la pagina  todos los videos
def videos(request):
    videos = Videos.objects.all()
    return render(request, 'paginas/videos.html', {'videos': videos})
   


# vista de la pagina de administracion
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
    
    