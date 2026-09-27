from django.contrib import admin
from .models import Cliente, Etiqueta, Transaccion, Cuenta


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'email',
        'telefono',
        'fecha_registro'
    )
    search_fields = (
        'nombre',
        'email',
        'telefono'
    )

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = (
        'numero_cuenta',
        'mostrar_clientes',
        'saldo',
        'fecha_creacion',
        'etiqueta'
    )
    search_fields = (
        'clientes__nombre',
        'numero_cuenta'
    )
    filter_horizontal = ('clientes',)  

    def mostrar_clientes(self, obj):
        return ", ".join(c.nombre for c in obj.clientes.all())
    mostrar_clientes.short_description = 'Clientes'

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = (
        'cuenta',
        'tipo',
        'monto',
        'fecha',
        'descripcion'
    )
    search_fields = (
        'cuenta__numero_cuenta',
        'tipo',
        'descripcion'
    )
# Register your models here.
