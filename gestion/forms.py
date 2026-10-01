from django import forms
from .models import Cliente, PerfilCliente, Cuenta
from django.contrib.auth.forms import AuthenticationForm

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'email',
            'telefono'
        ]
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'palceholder': 'Nombre completo',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'palceholder': 'correo@ejemplo.com',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'palceholder': '+56 9 1234 5678',
                }
            ),
        }
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control aw-input',
                'placeholder':'Usuario',
                'autofocus': True,
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control aw-input',
                'placeholder': 'Contrasena',
            }
        )
    )

class PerfilClienteForm(forms.ModelForm):
    class Meta:
        model = PerfilCliente
        fields = ['cliente', 'rut', 'direccion']

    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente')
        query = PerfilCliente.objects.filter(cliente=cliente)
        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError(f"El cliente '{cliente.nombre}' ya tiene un perfil registrado.")
        return cliente
    
class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['clientes', 'numero_cuenta', 'saldo', 'etiqueta']
        widgets = {
            'clientes': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si la cuenta ya existe (edición) y tiene transacciones, bloquea campos sensibles
        if self.instance.pk and self.instance.transacciones.exists():
            self.fields['numero_cuenta'].disabled = True
            self.fields['saldo'].disabled = True
            self.fields['saldo'].help_text = "El saldo no se edita directamente; se actualiza mediante transacciones."

    def clean_clientes(self):
        clientes = self.cleaned_data.get('clientes')
        if not clientes:
            raise forms.ValidationError("Debes asignar al menos un cliente a la cuenta.")
        return clientes

    def clean_numero_cuenta(self):
        numero = self.cleaned_data.get('numero_cuenta', '').strip().upper()
        query = Cuenta.objects.filter(numero_cuenta__iexact=numero)
        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError("Ya existe una cuenta con este número (no distingue mayúsculas de minúsculas).")
        return numero

'''from django import forms
from .models import Cliente, Cuenta, Etiqueta, Transaccion


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['clientes', 'numero_cuenta', 'saldo', 'etiqueta']
        widgets = {
            'clientes': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'numero_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'saldo': forms.NumberInput(attrs={'class': 'form-control'}),
            'etiqueta': forms.Select(attrs={'class': 'form-control'}),
        }


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['cuenta', 'tipo', 'monto', 'descripcion']
        widgets = {
            'cuenta': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }'''