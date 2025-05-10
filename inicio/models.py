from django.db import models

class Rol(models.Model):
    tipoRol = models.CharField(max_length=45)
    def str(self):
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

    def str(self):
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):
    nombreProducto = models.CharField(max_length=45)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def str(self):
        return self.nombreProducto

class Reserva(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    cantidadPersonas = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def str(self):
        return f"Reserva {self.id} - {self.fecha} {self.hora}"

class BebidaCaliente(models.Model):
    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,
        primary_key=True
    )
    TIPOS_BEBIDA = [
        ('CAFE', 'Café'),
        ('TE', 'Té'),
        ('CHOCOLATE', 'Chocolate caliente'),
        ('INFUSION', 'Infusión'),
    ]
    tipo = models.CharField(
        max_length=50,
        choices=TIPOS_BEBIDA,
        default='CAFE'
    )
    # ... otros campos específicos de bebidas ...