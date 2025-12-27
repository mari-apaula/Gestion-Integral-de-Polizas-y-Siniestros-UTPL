document.addEventListener('DOMContentLoaded', function () {
    const sidebarAdmin = document.querySelector('.sidebar-admin');
    const logoAdminImg = document.getElementById('logo-admin-sidebar');
    const body = document.body;


    const btnLogout = document.getElementById('btnLogout');

    // 1. Verificación de seguridad global
    // Esto asegura que si alguien entra al dashboard sin token, sea expulsado

    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/';
    }

    // 2. Lógica de Cerrar Sesión (Igual a la anterior)
    if (btnLogout) {
        btnLogout.addEventListener('click', async function () {
            localStorage.removeItem('access_token');
            localStorage.removeItem('userRole');

            // Avisar al backend que cierre la sesión
            await fetch('/logout/');

            window.location.href = '/';
        });
    }




    if (logoAdminImg && sidebarAdmin && body) {
        logoAdminImg.addEventListener('click', function () {
            sidebarAdmin.classList.toggle('compact-admin');
            body.classList.toggle('sidebar-admin-compacted');
        });
    }

    const navItems = document.querySelectorAll('.sidebar-admin .nav-links .nav-item');

    navItems.forEach(item => {
        item.addEventListener('click', function (event) {
            if (this.getAttribute('href') === '#') {
                event.preventDefault();
                if (this.getAttribute('href') === '#') {
                    event.preventDefault();
                }
            }

            navItems.forEach(nav => nav.classList.remove('active'));


            this.classList.add('active');


            const sectionTitle = document.getElementById('section-title-admin');
            if (sectionTitle) {
                const itemText = this.querySelector('span').textContent;
                sectionTitle.textContent = itemText;
            }
        });
    });

    const dashboardNavItem = document.getElementById('nav-dashboard-admin');
    if (dashboardNavItem) {
        dashboardNavItem.classList.add('active');
        const sectionTitle = document.getElementById('section-title-admin');
        if (sectionTitle) {
            sectionTitle.textContent = dashboardNavItem.querySelector('span').textContent;
        }
    }
});