from django.views.generic import FormView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .forms import LoginForm
from .services import AuthService
from django.views.generic import TemplateView
from .repositories import UsuarioRepository
import json

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from django.contrib.auth import login

from django.contrib.auth import logout

@method_decorator(csrf_exempt, name='dispatch')
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})

class LoginView(FormView): 
    template_name = 'login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                user, rol = AuthService.login_universal(
                    form.cleaned_data['username'], 
                    form.cleaned_data['password']
                )
                
                login(request, user)
                
                if rol == 'admin':
                    redirect_url = '/administrador/dashboard/'
                else:
                    redirect_url = '/dashboard-analista/'
                
                return JsonResponse({
                    'success': True,
                    'redirect_url': redirect_url
                }, status=200)

            except ValidationError as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'error': "Error interno"}, status=500)
        return JsonResponse({'success': False, 'error': "Datos inválidos"}, status=400)


class DashboardAdminView(LoginRequiredMixin, TemplateView):
    template_name = 'administrador/dashboard_admin.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if request.user.rol != 'admin':
            return redirect('dashboard_analista')
            
        return super().dispatch(request, *args, **kwargs)

class AdminUsuariosView(LoginRequiredMixin, TemplateView):
    template_name = 'administrador/usuarios.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
            
        if request.user.rol != 'admin':
            return redirect('dashboard_analista')
            
        return super().dispatch(request, *args, **kwargs)  


class DashboardAnalistaView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'       



@method_decorator(csrf_exempt, name='dispatch')
class UsuarioCRUDView(LoginRequiredMixin, View):
    """
    Vista centralizada para gestionar el CRUD de usuarios mediante JSON.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Si no está autenticado, responder 401 (Unauthorized)
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'No autenticado'}, status=401)
        
        # Si no es admin, responder 403 (Forbidden)
        if request.user.rol != 'admin':
            return JsonResponse({'error': 'No tienes permisos de administrador'}, status=403)
            
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, usuario_id=None):
        """LISTAR: Retorna todos los usuarios o uno específico."""
        if usuario_id:
            usuario = UsuarioRepository.get_by_id(usuario_id) 
            if not usuario:
                return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
            data = {
                'id': usuario.id, 'username': usuario.username, 'email': usuario.email,
                'rol': usuario.rol, 'cedula': usuario.cedula, 'estado': usuario.estado
            }
        else:
            usuarios = UsuarioRepository.get_all_usuarios()
            data = list(usuarios.values('id', 'username', 'email', 'rol', 'cedula', 'estado'))
        
        return JsonResponse(data, safe=False)

    def post(self, request):
        """CREAR: Recibe JSON para crear un nuevo usuario."""
        try:
            data = json.loads(request.body)
            user = UsuarioRepository.create_usuario(data)
            return JsonResponse({
                'success': True,
                'message': 'Usuario creado exitosamente',
                'id': user.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    def put(self, request, usuario_id):
        """ACTUALIZAR: Modifica un usuario existente."""
        try:
            data = json.loads(request.body)
            usuario = UsuarioRepository.update_usuario(usuario_id, data)
            return JsonResponse({
                'success': True,
                'message': f'Usuario {usuario.username} actualizado'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    def delete(self, request, usuario_id):
        """ELIMINAR: Borra un usuario del sistema."""
        try:
            UsuarioRepository.delete_usuario(usuario_id)
            return JsonResponse({
                'success': True, 
                'message': 'Usuario eliminado correctamente'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)    