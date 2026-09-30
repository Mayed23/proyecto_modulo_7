from django.urls import path
from .views import (
    ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
    PerfilClienteCreateView, PerfilClienteUpdateView, PerfilClienteListView, PerfilClienteDeleteView,
)

urlpatterns = [
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/nuevo/', ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', ClienteDeleteView.as_view(), name='cliente_delete'),

    path('perfiles/', PerfilClienteListView.as_view(), name='perfil_list'),
    path('perfiles/nuevo/', PerfilClienteCreateView.as_view(), name='perfil_create'),
    path('perfiles/<int:pk>/editar/', PerfilClienteUpdateView.as_view(), name='perfil_update'),
    path('perfiles/<int:pk>/eliminar/', PerfilClienteDeleteView.as_view(), name='perfil_delete'),
]

