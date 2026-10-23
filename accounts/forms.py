from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu usuário'
        })
    )

    password = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha'
        })
    )



from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


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