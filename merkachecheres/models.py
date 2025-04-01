from django.db import models

# Create your models here.
from django.db import models

class Usuario(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    ROLES = (
        (1, "Admin"),
        (2, "Cliente"),
        (3, "Vendedor")
    )
    rol = models.IntegerField(choices=ROLES, default=2)
    
    def __str__(self):
        return self.username
