from django.contrib import admin
from django.urls import path
from visitantes.views import (
    registrar_visitante, 
    informacoes_visitante, 
    finalizar_visita, 
    alterar_status_visitante, 
    listar_visitantes, 
    index
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rota para a página inicial (index)
    path('', index, name="index"),
    
    # Rotas para o CRUD de visitantes
    path('registrar-visitante/', registrar_visitante, name="registrar_visitante"),
    path('informacoes-visitante/<int:id>/', informacoes_visitante, name='informacoes_visitante'),
    path('visitantes/<int:id>/finalizar-visita/', finalizar_visita, name='finalizar_visita'),
    path('visitantes/<int:id>/alterar-status/', alterar_status_visitante, name='alterar_status_visitante'),
    
    # Rotas para autenticação
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Lista de visitantes
    path('visitantes/', listar_visitantes, name='listar_visitantes'),
]
