# from django.views import generic

# from django.views.generic import FormView
# class ProductFormView(generic.FormView):
#     template_name = "productos/add_product.html"

from django.views import generic
from productos.forms import ProductForm
from django.conf import settings
import os
from django.urls import reverse_lazy 


class ProductFormView(generic.FormView):      
    template_name = "productos/add_product.html"
    form_class = ProductForm
    success_url = reverse_lazy('add_product')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ProductListView(generic.ListView):
    template_name = "productos/list_products.html"
    context_object_name = "products"
    model = Product

    
    """"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Imprimir información de depuración
        print("Template Dirs:", settings.TEMPLATES[0]['DIRS'])
        print("Buscando template:", self.template_name)
        print("¿Existe el archivo?", os.path.exists(r"D:\Mis documentos\Escritorio\proyectos\coffee_shop\products\templates\productos\add_product.html"))
        return context"""