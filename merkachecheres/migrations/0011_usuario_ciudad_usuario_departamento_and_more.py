# Generated by Django 5.1.6 on 2025-04-06 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merkachecheres', '0010_usuario_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='ciudad',
            field=models.CharField(default='Sin ciudad', max_length=100),
        ),
        migrations.AddField(
            model_name='usuario',
            name='departamento',
            field=models.CharField(default='Sin departamento', max_length=100),
        ),
        migrations.AddField(
            model_name='usuario',
            name='direccion',
            field=models.CharField(default='Sin dirección', max_length=255),
        ),
        migrations.AddField(
            model_name='usuario',
            name='municipio',
            field=models.CharField(default='Sin municipio', max_length=100),
        ),
        migrations.AddField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(default='Sin teléfono', max_length=15),
        ),
    ]
