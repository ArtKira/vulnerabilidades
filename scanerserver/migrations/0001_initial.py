# Generated by Django 4.1.6 on 2023-04-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('device_type', models.CharField(max_length=100)),
                ('ip_address', models.GenericIPAddressField()),
                ('mac_address', models.CharField(max_length=17)),
                ('manufacturer', models.CharField(max_length=100)),
            ],
        ),
    ]
