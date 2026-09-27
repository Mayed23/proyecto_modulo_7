from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Cuenta(models.Model):
    clientes = models.ManyToManyField(
        Cliente, related_name='cuenta'
    )
    numero_cuenta = models.CharField(max_length=30, unique=True)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    etiqueta = models.OneToOneField(
        Etiqueta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cuenta'
    )

    def __str__(self):
        return self.numero_cuenta


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