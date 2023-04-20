from django.db import models

# Create your models here.

# Modelo para arp_scan

class Device(models.Model):
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17)
    manufacturer = models.CharField(max_length=100)

    def __str__(sefl):
        return sefl.name