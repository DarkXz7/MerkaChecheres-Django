# Generated by Django 5.1.1 on 2025-04-03 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merkachecheres', '0007_remove_producto_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='dimensiones',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
