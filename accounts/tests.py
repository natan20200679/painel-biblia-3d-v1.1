from django.test import TestCase
from django.contrib.auth import get_user_model
from .forms import LoginForm
from django.urls import reverse


Usuario = get_user_model()


class LoginTestCase(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='aluno_teste',
            email='aluno@teste.com',
            password='SenhaTeste123!',
            tipo='ALUNO'
        )

    def test_login_com_credenciais_validas(self):
        form = LoginForm(
            data={
                'username': 'aluno_teste',
                'password': 'SenhaTeste123!'
            }
        )

        self.assertTrue(form.is_valid())

    def test_login_com_senha_incorreta(self):
        form = LoginForm(
            data={
                'username': 'aluno_teste',
                'password': 'senha_errada'
            }
        )

        self.assertFalse(form.is_valid())

    def test_usuario_padrao_e_aluno(self):
        novo_usuario = Usuario.objects.create_user(
            username='outro_aluno',
            password='OutraSenha123!'
        )

        self.assertEqual(novo_usuario.tipo, 'ALUNO')



class PermissoesTestCase(TestCase):

    def setUp(self):
        self.aluno = Usuario.objects.create_user(
            username='aluno',
            password='SenhaAluno123!',
            tipo='ALUNO'
        )

        self.instituicao = Usuario.objects.create_user(
            username='instituicao',
            password='SenhaInstituicao123!',
            tipo='INSTITUICAO'
        )

    def test_aluno_acessa_sua_area(self):
        self.client.force_login(self.aluno)

        resposta = self.client.get(
            reverse('area_aluno')
        )

        self.assertEqual(resposta.status_code, 200)

    def test_aluno_nao_acessa_area_instituicao(self):
        self.client.force_login(self.aluno)

        resposta = self.client.get(
            reverse('area_instituicao')
        )

        self.assertEqual(resposta.status_code, 403)

    def test_instituicao_acessa_sua_area(self):
        self.client.force_login(self.instituicao)

        resposta = self.client.get(
            reverse('area_instituicao')
        )

        self.assertEqual(resposta.status_code, 200)

    def test_usuario_nao_autenticado_nao_acessa_area_aluno(self):
        resposta = self.client.get(
            reverse('area_aluno')
        )

        self.assertEqual(resposta.status_code, 302)



class FluxoAutenticacaoTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='aluno_fluxo',
            email='fluxo@teste.com',
            password='VentoAzul#2026',
            tipo='ALUNO'
        )

    def test_cadastro_cria_aluno(self):
        resposta = self.client.post(
            reverse('cadastro'),
            {
                'username': 'aluno_novo',
                'email': 'novo@teste.com',
                'password1': 'VentoAzul#2026',
                'password2': 'VentoAzul#2026',
            }
        )

        self.assertEqual(resposta.status_code, 201)

        novo_usuario = Usuario.objects.get(
            username='aluno_novo'
        )
        self.assertEqual(novo_usuario.tipo, 'ALUNO')

    def test_login_cria_sessao(self):
        resposta = self.client.post(
            reverse('login'),
            {
                'username': 'aluno_fluxo',
                'password': 'VentoAzul#2026',
            }
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(
            '_auth_user_id' in self.client.session
        )

    def test_login_com_senha_incorreta_falha(self):
        resposta = self.client.post(
            reverse('login'),
            {
                'username': 'aluno_fluxo',
                'password': 'senha_errada',
            }
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertFalse(
            '_auth_user_id' in self.client.session
        )

    def test_logout_encerra_sessao(self):
        self.client.force_login(self.usuario)

        resposta = self.client.post(reverse('logout'))

        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(
            '_auth_user_id' in self.client.session
        )

    def test_logout_recusa_requisicao_get(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(reverse('logout'))

        self.assertEqual(resposta.status_code, 405)
        self.assertTrue(
            '_auth_user_id' in self.client.session
        )

    
    def test_cadastro_publico_nao_cria_instituicao(self):
        resposta = self.client.post(
            reverse('cadastro'),
            {
                'username': 'tentativa_admin',
                'email': 'admin@teste.com',
                'password1': 'VentoAzul#2026',
                'password2': 'VentoAzul#2026',
                'tipo': 'INSTITUICAO',
            }
        )

        self.assertEqual(resposta.status_code, 201)

        usuario = Usuario.objects.get(
            username='tentativa_admin'
        )

        self.assertEqual(usuario.tipo, 'ALUNO')