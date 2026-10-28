from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('aluno/', views.area_aluno, name='area_aluno'),
    path('instituicao/', views.area_instituicao, name='area_instituicao'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('api/status/', views.status_api, name='status_api'),
]