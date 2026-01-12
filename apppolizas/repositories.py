from .models import Usuario, Poliza, Siniestro, Factura, DocumentoSiniestro, ResponsableCustodio
from django.shortcuts import get_object_or_404

class UsuarioRepository:
    """Repositorio para operaciones de acceso a datos de Usuario"""

    @staticmethod
    def get_by_username(username: str):
        """Buscar usuario por nombre de usuario"""
        try:
            return Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def get_by_id(usuario_id):
        try:
            return Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return None        

    @staticmethod
    def get_all_usuarios():
        return Usuario.objects.all()

    @staticmethod
    def create_usuario(data):
        return Usuario.objects.create_user(**data)

    @staticmethod
    def update_usuario(usuario_id, data):
        usuario = Usuario.objects.get(id=usuario_id)
        for key, value in data.items():
            setattr(usuario, key, value)
        usuario.save()
        return usuario

    @staticmethod
    def delete_usuario(usuario_id):
        Usuario.objects.filter(id=usuario_id).delete()        

class PolizaRepository:
    """Repositorio para operaciones de acceso a datos de Pólizas"""

    @staticmethod
    def get_all():
        return Poliza.objects.all().order_by('-fecha_registro')

    @staticmethod
    def get_by_id(poliza_id):
        try:
            return Poliza.objects.get(id=poliza_id)
        except Poliza.DoesNotExist:
            return None

    @staticmethod
    def create(data):
        return Poliza.objects.create(**data)

    @staticmethod
    def update(poliza, data):
        for field, value in data.items():
            setattr(poliza, field, value)
        poliza.save()
        return poliza

    @staticmethod
    def delete(poliza):
        poliza.delete()

class SiniestroRepository:
    @staticmethod
    def get_all():
        return Siniestro.objects.all().order_by('-fecha_siniestro')

    @staticmethod
    def get_by_poliza(poliza_id):
        return Siniestro.objects.filter(poliza_id=poliza_id).order_by('-fecha_siniestro')

    @staticmethod
    def get_by_id(id):
        return Siniestro.objects.filter(id=id).first()

    @staticmethod
    def create(poliza, data, usuario):
        # Creamos la instancia manualmente para tener control total
        siniestro = Siniestro(
            poliza=poliza,
            
            # Asignamos el Custodio que viene del formulario
            custodio=data.get('custodio'), 
            
            # Datos básicos
            fecha_siniestro=data.get('fecha_siniestro'),
            tipo_siniestro=data.get('tipo_siniestro'),
            ubicacion_bien=data.get('ubicacion_bien'),
            causa_siniestro=data.get('causa_siniestro'),
            nombre_bien=data.get('nombre_bien'),
            
            # Datos de auditoría
            usuario_gestor=usuario,
            estado_tramite='REPORTADO' # Estado inicial por defecto
        )
        siniestro.save()
        return siniestro

    @staticmethod
    def update(siniestro_id, data):
        siniestro = get_object_or_404(Siniestro, id=siniestro_id)
        
        # Actualizamos campos permitidos
        siniestro.fecha_siniestro = data.get('fecha_siniestro')
        siniestro.tipo_siniestro = data.get('tipo_siniestro')
        siniestro.custodio = data.get('custodio') # Actualizar custodio si cambió
        siniestro.nombre_bien = data.get('nombre_bien')
        siniestro.ubicacion_bien = data.get('ubicacion_bien')
        siniestro.causa_siniestro = data.get('causa_siniestro')
        
        # Si vienen campos financieros/estado en el form de edición, los actualizamos
        if 'estado_tramite' in data:
            siniestro.estado_tramite = data.get('estado_tramite')
        
        siniestro.save()
        return siniestro
    
    
class FacturaRepository:
    """Repositorio para operaciones de acceso a datos de Facturas"""

    @staticmethod
    def get_all():
        # Ordenamos por fecha de emisión (más recientes primero)
        return Factura.objects.all().order_by('-fecha_emision')

    @staticmethod
    def get_by_id(factura_id):
        try:
            return Factura.objects.get(id=factura_id)
        except Factura.DoesNotExist:
            return None

    @staticmethod
    def create(data):
        # Al usar create(), Django llama internamente a save(), 
        # por lo que tus cálculos automáticos (IVA, descuentos) SE EJECUTARÁN.
        return Factura.objects.create(**data)




# DocumentoSiniestroRepository

class DocumentoRepository:
    
    @staticmethod
    def create(data, archivo, usuario):
        """
        Crea el registro en BD. 
        Nota: Django maneja la subida a MinIO automáticamente al llamar a .create() 
        gracias a la configuración del settings.py.
        """
        return DocumentoSiniestro.objects.create(
            siniestro=data['siniestro'],
            tipo=data['tipo'],
            descripcion=data.get('descripcion', ''),
            archivo=archivo, # El objeto archivo en memoria
            subido_por=usuario
        )

    @staticmethod
    def get_by_siniestro(siniestro_id):
        return DocumentoSiniestro.objects.filter(siniestro_id=siniestro_id).order_by('-fecha_subida')

    @staticmethod
    def delete(documento_id):
        # Al borrar el registro, django-storages también intenta borrar el archivo en MinIO
        return DocumentoSiniestro.objects.filter(id=documento_id).delete()
    

class CustodioRepository:
    """Repositorio para gestión de Responsables/Custodios"""

    @staticmethod
    def get_all():
        return ResponsableCustodio.objects.all().order_by('nombre_completo')

    @staticmethod
    def get_by_id(custodio_id):
        try:
            return ResponsableCustodio.objects.get(id=custodio_id)
        except ResponsableCustodio.DoesNotExist:
            return None

    @staticmethod
    def create(data):
        return ResponsableCustodio.objects.create(**data)

    @staticmethod
    def update(custodio, data):
        for field, value in data.items():
            setattr(custodio, field, value)
        custodio.save()
        return custodio

    @staticmethod
    def delete(custodio_id):
        return ResponsableCustodio.objects.filter(id=custodio_id).delete()