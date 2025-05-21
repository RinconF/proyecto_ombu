from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model


class usuario_manager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
    
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
# class Rol(models.Model):
#     tipoRol = models.CharField(max_length=45)
#     def __str__(self):
#         return self.tipoRol

# class Categoria(models.Model):
#     nombreCategoria = models.CharField(max_length=50)
#     def __str__(self):
#         return self.nombreCategoria

    def crear_user(self, email, username, password=None, **extra_fields):
        """Alias para mantener compatibilidad con código existente"""
        return self.create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('rol', 'Administrador')
    
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)

    def crear_superuser(self, email, username, password=None, **extra_fields):
        """Alias para mantener compatibilidad con código existente"""
        return self.create_superuser(email, username, password, **extra_fields)


class Usuario(AbstractUser):
    ROLES = (
        ('administrador', 'administrador'),
        ('mesero', 'mesero'),
    )
  
    email = models.EmailField(unique=True, default='sin_email@ejemplo.com')
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    rol = models.CharField(max_length=20, choices=ROLES, default='Mesero')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
  
    objects = usuario_manager()
  
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='grupos',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        related_name="usuario_set",
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='permisos de usuario',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        related_name="usuario_set",
        related_query_name="usuario",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class Mesa(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    
    def __str__(self):
        return f"Mesa {self.numero}"

class Pedidos(models.Model):
    fechahoraPedido = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    id_mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)  # Cambié IntegerField por ForeignKey
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pedido en mesa {self.id_mesa.numero} - ${self.precio}"  # Modifiqué para mostrar el número de la mesa



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
        return self.nombreProducto





class Reserva(models.Model):
    nombreperReserva = models.CharField(max_length=45, default="sin nombre")
    fecha = models.DateField()
    hora = models.TimeField()
    cantidadPersonas = models.IntegerField()
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reserva {self.id} - Mesa {self.mesa.numero} el {self.fecha} a las {self.hora}"

User = get_user_model()

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username