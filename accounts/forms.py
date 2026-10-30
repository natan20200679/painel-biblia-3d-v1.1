from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class LoginForm(AuthenticationForm):

    nome = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu usuário'
        })
    )

    senha = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha'
        })
    )


class CadastroForm(UserCreationForm):
    
    class Meta:
        model = Usuario
        fields = ['username', 'email']

    def save(self, commit=True):
        usuario = super().save(commit=False)

        usuario.tipo = Usuario.TipoUsuario.ALUNO

        if commit:
            usuario.save()

        return usuario