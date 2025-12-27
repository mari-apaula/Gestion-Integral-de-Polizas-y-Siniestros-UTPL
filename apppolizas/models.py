from django.db import models
from django.contrib.auth.models import AbstractUser



class Usuario(AbstractUser):
    # Heredamos id, username, password, email, first_name y last_name de AbstractUser

    ADMINISTRADOR = 'admin'
    ANALISTA = 'analista'
    
    TIPO_USUARIO_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (ANALISTA, 'Analista'),
    ]

    rol = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default=ANALISTA
    )

    cedula = models.IntegerField(unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} - {self.rol}"





class Poliza(models.Model):
    numero_poliza = models.CharField(max_length=50, unique=True)
    vigencia_inicio = models.DateField()
    vigencia_fin = models.DateField()
    monto_asegurado = models.IntegerField()
    tipo_poliza = models.CharField(max_length=100)
    prima_base = models.FloatField()  
    prima_total = models.FloatField()
    estado = models.CharField(max_length=20)
    renovable = models.BooleanField(default=False)
    fecha_emision = models.DateField()
    fecha_registro = models.DateField(auto_now_add=True)
    
    # RELACIÓN: Uno a Muchos (Un administrador gestiona muchas pólizas)
    usuario_gestor = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='polizas_gestionadas'
    )

    def __str__(self):
        return self.numero_poliza