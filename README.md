Módulo 7: Desarrollo Web con Django.

Tecnologías utilizadas

    Python 3.12
    Django 5.1
    MySQL (base de datos relacional)
    Bootstrap 5 + Bootstrap Icons (interfaz)
    JavaScript vanilla (sin dependencias externas de frontend)
    python-dotenv (variables de entorno)

Arquitectura del proyecto

alke_wallet/
├── alke_wallet/           # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── gestion/                # App principal
│   ├── models.py           # Cliente, PerfilCliente, Etiqueta, Cuenta, Transaccion
│   ├── forms.py            # Formularios con validaciones personalizadas
│   ├── views.py            # Vistas basadas en clases (CRUD)
│   ├── urls.py              # Rutas de la app
│   ├── admin.py              # Registro de modelos en el panel admin
│   ├── static/gestion/
│   │   ├── css/style.css    # Tema oscuro personalizado
│   │   └── js/main.js       # Interactividad (selectores, buscador, saldo en vivo)
│   └── templates/gestion/   # Templates de cada modelo (list, form, confirm_delete)
├── templates/registration/  # Login
├── .env                     # Variables de entorno (no versionado)
├── .gitignore
├── requirements.txt
└── manage.py

Modelo de datos

El proyecto implementa los tres tipos de relaciones del ORM de Django:

Relación	               Modelos	                  Tipo
___________________________________________________________________
Un cliente tiene            Cliente <->
un único perfil            PerfilCliente            OneToOne
con sus datos legales
____________________________________________________________________
Una cuenta tiene un tipo;   Cuente-->Etiqueta
muchas cuentas comparten    Transaccion-->Cuenta    ManyToOne
el mismo tipo. Una cuenta 
tiene muchas transacciones
_____________________________________________________________________
Un cliente puede tener           Cliente<-->Cuenta  ManyToMany           
varias cuentas; una cuenta 
puede tener varios titulares 
(cuenta conjunta)
_____________________________________________________________________




Resumen de modelos

Cliente: nombre, email, teléfono, fecha de registro, tipo (Persona Natural / Persona Jurídica).

PerfilCliente: RUT (único, no editable tras su creación) y dirección, asociado 1 a 1 con Cliente.

Etiqueta: tipo de cuenta (Ahorro, Corriente, u otros a futuro).

Cuenta: número de cuenta (único, sin distinguir mayúsculas/minúsculas), saldo, etiqueta, estado (activa/inactiva), clientes titulares (M2M). Incluye las propiedades calculadas es_conjunta, titularidad y puede_eliminarse.

Transaccion: tipo (depósito, retiro, transferencia), monto, descripción, cuenta de origen y, en transferencias, cuenta destino.

Accede a http://127.0.0.1:8000/ e inicia sesión con las credenciales creadas ya creadas: 
Usuario Admin
Contraseña: admin123

Uso del sistema

-El acceso es exclusivo para el operador/administrador de Alke Wallet — no existe registro público de usuarios (ver Decisiones de diseño). Tras iniciar sesión, el menú superior permite navegar entre:

-Clientes: listado con indicador de perfil completo/pendiente, saldo por tipo de cuenta, acceso rápido a edición y perfil.

-Cuentas: listado con saldo, titularidad (Personal/Jurídica/Conjunta) y tipo.

-Transacciones: historial filtrable por cuenta o cliente, con registro de nuevas operaciones.

-Etiquetas: gestión de los tipos de cuenta disponibles.

Funcionalidades principales

-CRUD completo (Crear, Leer, Actualizar, Eliminar) para Cliente, PerfilCliente, Cuenta y Etiqueta.

-Transacciones (Crear y Listar únicamente — por diseño, ver más abajo): depósitos, retiros y transferencias entre cuentas, con actualización automática de saldos.

-Transferencias: generan dos registros vinculados (emisor y receptor), mostrados con color y signo distintos (rojo/negativo para quien envía, verde/sin signo para quien recibe).

-Saldo en vivo: al seleccionar una cuenta en el formulario de transacción, se muestra su saldo disponible sin recargar la página.

-Filtros: historial de transacciones filtrable por cuenta o por cliente (vía GET, compartible por URL).
Autenticación: acceso protegido con django.contrib.auth y LoginRequiredMixin en todas las vistas.
Mensajes: confirmaciones y errores con django.contrib.messages.

Reglas de negocio y validaciones

-El número de cuenta debe ser único, sin distinguir mayúsculas de minúsculas.
-El saldo de una cuenta no se edita manualmente: solo cambia a través de transacciones.
-Una vez que una cuenta registra transacciones, su número y saldo quedan bloqueados en el formulario  de      edición.
-El RUT de un perfil de cliente no puede modificarse una vez registrado.
-No se puede eliminar una cuenta con saldo distinto de cero o con movimientos registrados (puede desactivarse en su lugar).
-No se puede eliminar un cliente si tiene cuentas con saldo, movimientos, o si su eliminación dejaría alguna cuenta sin titular.
-No se puede eliminar una etiqueta que esté en uso por alguna cuenta.
-Una transferencia valida que exista saldo suficiente y que la cuenta origen y destino no sean la misma.
-Las transacciones no se pueden editar ni eliminar una vez creadas: representan hechos históricos, consistente con el funcionamiento de un sistema financiero real.

Decisiones de diseño

-Sin registro público: el sistema está pensado como un panel de operador/administrador de Alke Financial, no como una app de cara al cliente final. Por eso no existe un formulario de alta de usuarios; las cuentas de acceso las crea el administrador desde /admin/.

-Etiqueta sin CRUD inicial, luego incorporado: el catálogo de tipos de cuenta (Ahorro, Corriente) es reducido y estable, por lo que en una primera etapa se gestionaba desde el panel de administración. Como el modelo Etiqueta es una entidad independiente relacionada con Cuenta (Many to One), se añadió posteriormente un CRUD completo sin modificar la estructura del modelo, demostrando la escalabilidad del diseño original.

-Transacciones inmutables: siguiendo el principio de integridad contable, una transacción no se puede editar ni eliminar. Cualquier corrección se realiza mediante una nueva transacción compensatoria.

Mejoras futuras

1.-Acceso diferenciado para clientes finales: vincular Cliente con el sistema de autenticación de Django (User) mediante una nueva relación One to One, de modo que cada cliente pueda loguearse y visualizar únicamente sus propias cuentas y transacciones, además de poder ejecutarlas dentro de los límites de sus propias cuentas. El botón "Registrarse", presente en la interfaz actual mas no conectado a ninguna vista, se dejó como referencia visual de esta funcionalidad planificada.

2.-Permisos diferenciados: uso de grupos de permisos de Django para distinguir entre operadores con acceso total y colaboradores con permisos limitados (por ejemplo, sin capacidad de eliminar registros).
Soporte de transferencias externas: incorporar un campo para datos bancarios externos, permitiendo transferencias hacia cuentas fuera del sistema.

3.-Notificaciones por correo: integrar django.core.mail para notificar a los clientes sobre movimientos en sus cuentas.