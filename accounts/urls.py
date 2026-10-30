from django.urls import path
from views import(login_view, logout_view, area_aluno, area_instituicao, cadastro_view, status_api)


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('aluno/', area_aluno, name='area_aluno'),
    path('instituicao/', area_instituicao, name='area_instituicao'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('api/status/', status_api, name='status_api'),
]