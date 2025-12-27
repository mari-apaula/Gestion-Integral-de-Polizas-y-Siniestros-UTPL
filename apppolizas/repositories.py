from .models import Usuario

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