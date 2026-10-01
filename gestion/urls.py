from django.urls import path
from .views import (
    ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
    PerfilClienteCreateView, PerfilClienteUpdateView, PerfilClienteListView, PerfilClienteDeleteView,
    CuentaCreateView, CuentaListView, CuentaUpdateView, CuentaDeleteView
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

    path('cuentas/', CuentaListView.as_view(), name='cuenta_list'),
    path('cuentas/nueva/', CuentaCreateView.as_view(), name='cuenta_create'),
    path('cuentas/<int:pk>/editar/', CuentaUpdateView.as_view(), name='cuenta_update'),
    path('cuentas/<int:pk>/eliminar/', CuentaDeleteView.as_view(), name='cuenta_delete'),
]

