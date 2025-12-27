import jwt
import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from .repositories import UsuarioRepository
from .models import Usuario

class AuthService:
    @staticmethod
    def login_universal(username, password):
        # 1. Validación de campos vacíos
        if not username or not password:
            raise ValidationError("Usuario y contraseña son obligatorios")

        # 2. Buscar usuario en la base de datos
        user = UsuarioRepository.get_by_username(username)
        
        # 3. Validar existencia y contraseña
        if not user or not user.check_password(password):
            raise ValidationError("Credenciales inválidas")

        # 4. REGLA DE SEGURIDAD: Verificar si el usuario está activo
        if not user.estado:
            raise ValidationError("Esta cuenta está desactivada. Contacte al administrador.")

        # 5. Generar JWT (El payload es correcto)
        payload = {
            'id': user.id,
            'username': user.username,
            'rol': user.rol,  # Esto devolverá 'admin' o 'analista'
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        
        # Retornamos el token y el valor crudo del rol ('admin'/'analista')
        return user, user.rol