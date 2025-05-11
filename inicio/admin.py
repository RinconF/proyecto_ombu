from django.contrib import admin
from .models import Rol, Categoria, Usuario, Producto, Mesa, Pedido, Reserva

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('tipoRol',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombreCategoria',)
    search_fields = ('nombreCategoria',)
    ordering      = ('nombreCategoria',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'apellido', 'correo', 'rol')
    search_fields = ('nombre', 'apellido', 'correo')
    list_filter   = ('rol',)
    ordering      = ('apellido',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display  = ('nombreProducto', 'precio', 'categoria')
    search_fields = ('nombreProducto',)
    list_filter   = ('categoria',)
    ordering      = ('nombreProducto',)

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero',)
    ordering     = ('numero',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display    = ('id', 'usuario', 'mesa', 'total', 'fecha')
    list_filter     = ('fecha', 'mesa')
    date_hierarchy  = 'fecha'

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display    = ('id', 'usuario', 'mesa', 'fecha', 'estado')
    list_filter     = ('estado', 'fecha')
    date_hierarchy  = 'fecha'