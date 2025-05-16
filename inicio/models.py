from django.db import models

class Rol(models.Model):
    tipoRol = models.CharField(max_length=45)

    def __str__(self):
        return self.tipoRol

class Categoria(models.Model):
    nombreCategoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreCategoria

class Usuario(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    correo = models.EmailField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=100)
    celular = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):
    nombreProducto = models.CharField(max_length=45)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreProducto

class Mesa(models.Model):
    numero = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Mesa {self.numero}"

class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='pedido')
    cantidad = models.IntegerField()
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - Total: {self.total}"

class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    fecha = models.DateField()
    hora = models.TimeField()
    cantidadPersonas = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='reserva')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        mesa_info = f"Mesa {self.mesa.numero}" if self.mesa else "Mesa no asignada"
        return f"Reserva {self.id} - {mesa_info} el {self.fecha} a las {self.hora}"
