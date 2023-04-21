from django import forms
from .models import Device


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

