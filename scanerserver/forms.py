from django import forms
from .models import Device
from django.contrib.auth.forms import AuthenticationForm



# Formulario arp_scan
from django import forms
from .models import Device

DEVICE_TYPE_CHOICES = (
    ('PC', 'PC'),
    ('Router', 'Router'),
    ('Servidor', 'Servidor'),
    ('Telefono', 'Telefono'),
)

# Formulario arp_scan
class DeviceForm(forms.ModelForm):
    device_type = forms.ChoiceField(choices=DEVICE_TYPE_CHOICES)

    class Meta:
        model = Device
        fields = ['name', 'device_type', 'ip_address', 'mac_address', 'manufacturer']


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'class': 'textfield'})
        self.fields['username'].widget.attrs['placeholder'] = 'Ingrese su usuario'
        self.fields['password'].widget.attrs['placeholder'] = 'Ingrese su contraseña'


