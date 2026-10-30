from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import LoginForm
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Usuario
from django.http import JsonResponse
from .forms import LoginForm
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

def login_view(request):
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('password')
        usuario = authenticate(request, nome = nome, senha = senha)
        if usuario is not None:
            auth_login(request, usuario)
            return redirect('login')
    
    return render(request, 'accounts/login.html') 

def tipo_usuario_required(tipo_permitido):
    def decorator(view_func):

        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.tipo != tipo_permitido:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


@tipo_usuario_required(Usuario.TipoUsuario.ALUNO)
def area_aluno(request):
    return JsonResponse({
        'mensagem': 'Acesso autorizado',
        'perfil': 'aluno',
        'usuario': request.user.username
    })


@tipo_usuario_required(Usuario.TipoUsuario.INSTITUICAO)
def area_instituicao(request):
    return JsonResponse({
        'mensagem': 'Acesso autorizado',
        'perfil': 'instituicao',
        'usuario': request.user.username
    })


from django.views.decorators.http import require_POST
from .forms import CadastroForm


@require_POST
def cadastro_view(request):
    form = CadastroForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {
                'erro': 'Não foi possível realizar o cadastro.',
                'detalhes': form.errors.get_json_data(),
            },
            status=400
        )

    usuario = form.save()

    return JsonResponse(
        {
            'mensagem': 'Cadastro realizado com sucesso.',
            'usuario': usuario.username,
            'perfil': usuario.tipo,
        },
        status=201
    )

def logout_view(request):
    logout(request)

    return redirect('login')

def status_api(request):
    return JsonResponse({
        'projeto': 'Bíblia 3D',
        'status': 'online',
        'mensagem': 'Backend funcionando corretamente.'
    })