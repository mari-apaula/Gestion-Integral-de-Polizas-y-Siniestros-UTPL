document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Evita que la URL cambie y la página se recargue

            const formData = new FormData(loginForm);

            try {
                const response = await fetch('/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        // Extraemos el token CSRF de las cookies para que Django acepte la petición
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    // Guardamos el token y el rol en el navegador
                    localStorage.setItem('access_token', data.token);
                    localStorage.setItem('userRole', data.rol);
                    
                    // Redirigimos según lo que diga el servidor
                    window.location.href = data.redirect_url;
                } else {
                    alert(data.error || 'Credenciales incorrectas');
                }

            } catch (error) {
                console.error('Error:', error);
                alert('Error de conexión con el servidor');
            }
        });
    }
});

// Función para obtener el CSRF token de las cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}