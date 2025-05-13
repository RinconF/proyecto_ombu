from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario


class customusuario_crear(UserCreationForm):
    class Meta:
        model = Usuario 
        fields = ('username','first_name', 'last_name', 'email', 'rol')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellido"
        
        for field_name, field in self.fields.items():
           field.widget.attrs['class'] = 'form-control'   #aplicar bootstrap
           
class customusuario_change(UserChangeForm):
    password = None #Esto evita que se muestre la contraseña al momento de editar
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_active')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellido"
        self.fields['is_active'].label = "Estado activo"
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  #bootstrap
            


class PasswordChangeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Nueva Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirmar Contraseña")
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data