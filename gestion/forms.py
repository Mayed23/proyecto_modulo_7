from django import forms
from .models import Cliente, PerfilCliente, Cuenta, Transaccion, Etiqueta
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el perfil ya existe (edición), el RUT no se puede modificar
        if self.instance.pk:
            self.fields['rut'].disabled = True
            self.fields['rut'].help_text = "El RUT no se puede modificar una vez registrado."

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

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['cuenta', 'tipo', 'cuenta_destino', 'monto', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cuentas_validas = Cuenta.objects.filter(activa=True).exclude(clientes__isnull=True).distinct()
        self.fields['cuenta'].queryset = cuentas_validas
        self.fields['cuenta_destino'].queryset = cuentas_validas
        self.fields['cuenta_destino'].required = False
        self.fields['cuenta'].label_from_instance = self._etiqueta_cuenta
        self.fields['cuenta_destino'].label_from_instance = self._etiqueta_cuenta

    @staticmethod
    def _etiqueta_cuenta(cuenta):
        tipo = cuenta.etiqueta.nombre if cuenta.etiqueta else "Sin tipo"
        titular = cuenta.clientes.first()
        nombre_titular = titular.nombre if titular else "Sin titular"
        return f"{cuenta.numero_cuenta} — {tipo} — {nombre_titular}"

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor a cero.")
        return monto

    def clean(self):
        cleaned_data = super().clean()
        cuenta = cleaned_data.get('cuenta')
        cuenta_destino = cleaned_data.get('cuenta_destino')
        tipo = cleaned_data.get('tipo')
        monto = cleaned_data.get('monto')

        if tipo == 'retiro' and cuenta and monto:
            if monto > cuenta.saldo:
                raise forms.ValidationError(
                    f"Saldo insuficiente. La cuenta '{cuenta.numero_cuenta}' tiene ${cuenta.saldo}."
                )

        if tipo == 'transferencia':
            if not cuenta_destino:
                raise forms.ValidationError("Debes indicar la cuenta destino para una transferencia.")
            if cuenta == cuenta_destino:
                raise forms.ValidationError("La cuenta origen y destino no pueden ser la misma.")
            if cuenta and monto and monto > cuenta.saldo:
                raise forms.ValidationError(
                    f"Saldo insuficiente en '{cuenta.numero_cuenta}' para transferir ${monto}."
                )

        return cleaned_data
class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ahorro, Corriente, Nómina'}),
        }