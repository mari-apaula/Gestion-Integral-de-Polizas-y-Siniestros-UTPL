document.addEventListener('DOMContentLoaded', function() {
    // 1. Verificación de Seguridad (Basada en tu código original)
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/'; 
    }

    // 2. Lógica de Cerrar Sesión
    // El ID 'btnLogout' debe estar presente en el sidebar del masteradmin
    const btnLogout = document.getElementById('btnLogout');
    if (btnLogout) {
        btnLogout.addEventListener('click', function() {
            localStorage.removeItem('access_token');
            alert('Sesión cerrada correctamente');
            window.location.href = '/';
        });
    }
});