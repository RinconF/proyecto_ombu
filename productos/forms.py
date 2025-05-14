from django import forms
from .models import Producto


class ProductForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label="Nombre")
    description = forms.CharField(max_length=300, label="Descripción")
    price = forms.DecimalField(max_digits=10, decimal_places=2, label="Precio")
    available = forms.BooleanField(initial=True, label="Disponible", required=False)
    photo = forms.ImageField(label="Foto", required=False)
    
    class Meta:
        model = Producto
        fields = ['name', 'description', 'price', 'available', 'photo','categoria']

    def save(self, commit=True):  # buena práctica
        producto = super().save(commit=False)
        if commit:
            producto.save()
        return producto
    
    # def save(self):
    #     Producto.objects.create(
    #         name=self.cleaned_data["name"],
    #         description=self.cleaned_data["description"],
    #         price=self.cleaned_data["price"],
    #         available=self.cleaned_data["available"],
    #         photo=self.cleaned_data["photo"],
    #     )
