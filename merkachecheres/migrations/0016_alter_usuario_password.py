# Generated by Django 5.1.1 on 2025-04-10 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merkachecheres', '0015_alter_imagenproducto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
