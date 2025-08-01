from django.shortcuts import redirect, render
from .models import Videos , Person
# Create your views here.

def index(request):
    return render(request, 'paginas/index.html')

def videos(request):
    videos = Videos.objects.all()
    return render(request, 'paginas/videos.html', {'videos': videos})
   

def administrador(request):
    video = Videos.objects.all()
    return render(request, 'paginas/admin.html', {'video': video})
    

def video_regis(request):
    if request.method == 'POST':
        video = Videos()
        
       
        video.video_name = request.POST.get('name')
        
        
        video.location = request.FILES.get('video')
        
        video.save()
        print("Video registrado:", video.video_name)
        return redirect('administrador')  
    


def personas(request):
    # Renombrado a 'videos' para mayor claridad y consistencia.
    person = Person.objects.all()
    return render(request, 'paginas/personas.html', {'person': person})


def editar_persona_admin(request):
    if request.method == 'POST':
        id_persona = request.POST.get('id_persona')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        
        persona = Person.objects.get(id_persona=id_persona)
        persona.nombre = nombre
        persona.apellido = apellido
        persona.correo = correo
        persona.telefono = telefono
        persona.save()
        
        return redirect('personas')  # Redirige a la vista de personas después de editar
    
from django.shortcuts import render, get_object_or_404

def editar(request, id_persona):
    # Usamos get_object_or_404 para manejar automáticamente el caso en que la persona no existe.
    # Si la persona no se encuentra, Django mostrará una página 404.
    persona_a_editar = get_object_or_404(Person, id_persona=id_persona)

    # Pasamos un único objeto 'persona_a_editar' al contexto del template.
    return render(request, 'modal/modal_persona_admin.html', {'persona_a_editar': persona_a_editar})