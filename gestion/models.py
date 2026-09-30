from django.db import models


class Cliente(models.Model):
    TIPO_CHOICES = [
        ('natural', 'Persona Natural'),
        ('juridica', 'Persona Jurídica'),
    ]
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    tipo_cliente = models.CharField(max_length=10, choices=TIPO_CHOICES, default='natural')

    def __str__(self):
        return self.nombre

class PerfilCliente(models.Model):
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    rut = models.CharField(max_length=12, unique=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.cliente.nombre}"


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Cuenta(models.Model):
    clientes = models.ManyToManyField(
        Cliente, related_name='cuentas'
    )
    numero_cuenta = models.CharField(max_length=30, unique=True)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    etiqueta = models.ForeignKey(
        Etiqueta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cuentas'
    )

    def __str__(self):
        return self.numero_cuenta

    @property
    def es_conjunta(self):
        return self.clientes.count() > 1

    @property
    def titularidad(self):
        if self.es_conjunta:
            return "Conjunta"
        cliente = self.clientes.first()
        if cliente and cliente.tipo_cliente == 'juridica':
            return "Jurídica"
        return "Personal"


class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('deposito', 'Depósito'),
        ('retiro', 'Retiro'),
        ('transferencia', 'Transferencia'),
    ]

    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.CASCADE,
        related_name='transacciones'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.monto} ({self.cuenta.numero_cuenta})"