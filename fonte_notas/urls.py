from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('note/', views.manage_notes, name='note_lista'),  # Para criar nova nota
    path('manage/<int:note_id>/', views.manage_notes, name='edit_note'),  # Para editar/excluir
]