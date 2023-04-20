from django import forms
from .models import Device


# Formulario arp_scan
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'device_type', 'ip_address', 'mac_address', 'manufacturer']
