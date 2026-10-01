from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cliente, PerfilCliente, Cuenta, Transaccion
from .forms import ClienteForm, PerfilClienteForm, CuentaForm


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'gestion/cliente_list.html'
    context_object_name = 'clientes'


class ClienteCreateView(LoginRequiredMixin, CreateView):
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
    form_class = ClienteForm
    template_name = 'gestion/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        messages.success(self.request, f"Cliente '{self.object.nombre}' actualizado correctamente.")
        return respuesta


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'gestion/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')

    def form_valid(self, form):
        cuentas_bloqueantes = self.object.cuentas.exclude(saldo=0)
        tiene_movimientos = Transaccion.objects.filter(cuenta__clientes=self.object).exists()
        cuentas_quedarian_huerfanas = [
            c for c in self.object.cuentas.all() if c.clientes.count() == 1
        ]

        if cuentas_bloqueantes.exists() or tiene_movimientos or cuentas_quedarian_huerfanas:
            messages.error(
                self.request,
                f"No se puede eliminar a '{self.object.nombre}': "
                f"tiene cuentas con saldo, movimientos, o quedarían sin titular."
            )
            return redirect('cliente_list')

        nombre = self.object.nombre
        respuesta = super().form_valid(form)
        messages.success(self.request, f"Cliente '{nombre}' eliminado correctamente.")
        return respuesta


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


class CuentaListView(LoginRequiredMixin, ListView):
    model = Cuenta
    template_name = 'gestion/cuenta_list.html'
    context_object_name = 'cuentas'
    paginate_by = 10
    ordering = ['numero_cuenta']


class CuentaCreateView(LoginRequiredMixin, CreateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = 'gestion/cuenta_form.html'
    success_url = reverse_lazy('cuenta_list')

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        messages.success(self.request, f"Cuenta '{self.object.numero_cuenta}' creada correctamente.")
        return respuesta


class CuentaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = 'gestion/cuenta_form.html'
    success_url = reverse_lazy('cuenta_list')

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        messages.success(self.request, f"Cuenta '{self.object.numero_cuenta}' actualizada correctamente.")
        return respuesta


class CuentaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cuenta
    template_name = 'gestion/cuenta_confirm_delete.html'
    success_url = reverse_lazy('cuenta_list')

    def form_valid(self, form):
        if not self.object.puede_eliminarse:
            messages.error(
                self.request,
                f"No se puede eliminar la cuenta '{self.object.numero_cuenta}': "
                f"tiene saldo o movimientos registrados."
            )
            return redirect('cuenta_list')

        numero = self.object.numero_cuenta
        respuesta = super().form_valid(form)
        messages.success(self.request, f"Cuenta '{numero}' eliminada correctamente.")
        return respuesta