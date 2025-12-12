from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        
        # Validaciones
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado')
            return redirect('register')
        
        # Crear usuario
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            
            # Redirigir al login después del registro exitoso
            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('signin')
                
        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
            return redirect('register')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales incorrectas. Inténtalo de nuevo.')
            return redirect('signin')
    
    return render(request, 'signin.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('signin')

@login_required(login_url='signin')
def dashboard_view(request):
    # Vista protegida - solo usuarios logueados pueden acceder
    return render(request, 'dashboard.html', {
        'user': request.user
    })