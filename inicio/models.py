from django.db import models

class Usuario(models.Model):
    ROLES = {
        ('ADM', 'Administrador'),
        ('MES', 'Mesero')
    }
    
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    correo = models.EmailField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=100)
    celular = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    rol = models.CharField( max_length=3, choices=ROLES, default='ADM')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Pedidos(models.Model):
    fechahoraPedido = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    id_mesa = models.IntegerField()
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return f"Pedido en mesa {self.id_mesa} - ${self.precio}"


class Producto(models.Model):
    nombreProducto = models.CharField(max_length=45)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    Pedidos = models.ForeignKey(Pedidos, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreProducto




class Inventario(models.Model):
    nombreProducto = models.CharField(max_length=45)
    Cantidad = models.CharField(max_length=50)
    precioProducto = models.DecimalField(max_digits=10, decimal_places=2)
    Producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombreCategoria





class Reserva(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    cantidadPersonas = models.IntegerField()
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reserva {self.id} - {self.fecha} {self.hora}"


