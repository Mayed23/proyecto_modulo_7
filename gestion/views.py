from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cliente, PerfilCliente
from .forms import ClienteForm, PerfilClienteForm

class ClienteListView(LoginRequiredMixin,ListView):
    model = Cliente
    template_name = 'gestion/cliente_list.html'
    context_object_name = 'clientes'
    
class ClienteCreateView(LoginRequiredMixin,CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        messages.success(self.request, f"Cliente '{self.object.nombre}' creado con éxito.")
        return respuesta

    def form_invalid(self, form):
        messages.error(self.request, "No se pudo guardar. Revisa los campos marcados en rojo.")
        return super().form_invalid(form)
    
class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class =  ClienteForm
    template_name = 'gestion/cliente_form.html'
    success_url = reverse_lazy('cliente_list')
    
class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'gestion/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')

class PerfilClienteListView(LoginRequiredMixin, ListView):
    model = PerfilCliente
    template_name = 'gestion/perfil_list.html'
    context_object_name = 'perfiles'


class PerfilClienteCreateView(LoginRequiredMixin, CreateView):
    model = PerfilCliente
    form_class = PerfilClienteForm
    template_name = 'gestion/perfil_form.html'
    success_url = reverse_lazy('cliente_list')

    def get_initial(self):
        initial = super().get_initial()
        cliente_id = self.request.GET.get('cliente')
        if cliente_id:
            initial['cliente'] = cliente_id
        return initial

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        messages.success(self.request, f"Perfil de '{self.object.cliente.nombre}' creado correctamente.")
        return respuesta


class PerfilClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = PerfilCliente
    form_class = PerfilClienteForm
    template_name = 'gestion/perfil_form.html'
    success_url = reverse_lazy('perfil_list')

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        messages.success(self.request, f"Perfil de '{self.object.cliente.nombre}' actualizado correctamente.")
        return respuesta


class PerfilClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = PerfilCliente
    template_name = 'gestion/perfil_confirm_delete.html'
    success_url = reverse_lazy('perfil_list')

    def form_valid(self, form):
        nombre = self.object.cliente.nombre
        respuesta = super().form_valid(form)
        messages.success(self.request, f"Perfil de '{nombre}' eliminado correctamente.")
        return respuesta
# Create your views here.
