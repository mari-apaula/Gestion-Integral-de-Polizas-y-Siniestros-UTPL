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
    

class Siniestro(models.Model):
    # Identificación del Siniestro 
    numero_reclamo = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    # RELACIÓN 1: Agregación (1 Póliza -> * Siniestros)
    # Se usa ForeignKey para representar la multiplicidad 1 a muchos desde la Póliza.
    poliza = models.ForeignKey(
        Poliza, 
        on_delete=models.CASCADE, 
        related_name='siniestros'
    )
    # RELACIÓN 2: Asociación (1 Usuario -> * Siniestros)
    # El usuario que gestiona o registra el siniestro.
    usuario_gestor = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='siniestros_gestionados'
    )

    # Datos clave del siniestro y del bien afectado [cite: 88, 91, 93]
    fecha_siniestro = models.DateField()
    tipo_siniestro = models.CharField(max_length=100) # Ej: Robo, Incendio, Daños
    ubicacion_bien = models.CharField(max_length=255)
    causa_siniestro = models.TextField()
    
    # Detalles del bien asegurado [cite: 88, 91]
    nombre_bien = models.CharField(max_length=100)
    marca = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    serie = models.CharField(max_length=50, null=True, blank=True)
    codigo_activo = models.CharField(max_length=50, null=True, blank=True)
    responsable_custodio = models.CharField(max_length=150) # [cite: 92]

    # Estado y Gestión del Trámite [cite: 87]
    ESTADO_CHOICES = [
        ('REPORTADO', 'Reportado'),
        ('DOCUMENTACION', 'En validación de documentos'),
        ('ENVIADO_ASEGURADORA', 'Enviado a Aseguradora'),
        ('LIQUIDADO', 'Liquidado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    estado_tramite = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='REPORTADO')
    fecha_notificacion = models.DateField(auto_now_add=True) # Fecha inicial del reporte [cite: 86]
    cobertura_aplicada = models.CharField(max_length=100, null=True, blank=True) # [cite: 87]

    # Datos de Liquidación y Finiquito 
    valor_reclamo = models.FloatField(default=0.0) # Valor total reclamado
    deducible_aplicado = models.FloatField(default=0.0)
    depreciacion = models.FloatField(default=0.0)
    valor_a_pagar = models.FloatField(default=0.0) # Valor final a pagar
