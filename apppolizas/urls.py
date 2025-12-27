from django.urls import path
from . import views

urlpatterns = [
    # Login y Dashboard Analista
    path('', views.LoginView.as_view(), name='login'),
    path('dashboard-analista/', views.DashboardAnalistaView.as_view(), name='dashboard_analista'),

    # --- ZONA ADMINISTRADOR ---
    # Vistas Visuales (HTML)
    path('administrador/dashboard/', views.DashboardAdminView.as_view(), name='dashboard_admin'),
    path('administrador/usuarios/', views.AdminUsuariosView.as_view(), name='admin_usuarios'),

    # API Endpoints (JSON para DataTables y Fetch)
    path('api/usuarios/', views.UsuarioCRUDView.as_view(), name='usuarios_list_create'),
    path('api/usuarios/<int:usuario_id>/', views.UsuarioCRUDView.as_view(), name='usuarios_detail'),

    path('logout/', views.logout_view, name='logout'),
]