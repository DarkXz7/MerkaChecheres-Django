# Generated by Django 5.1.6 on 2025-04-06 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merkachecheres', '0011_usuario_ciudad_usuario_departamento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='reset_token',
        ),
    ]
