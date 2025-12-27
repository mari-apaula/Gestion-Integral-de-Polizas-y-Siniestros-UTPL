// apppolizas/static/js/admin_usuarios.js

let dataTable;
const API_URL = '/api/usuarios/';

document.addEventListener('DOMContentLoaded', function() {
    initDataTable();
});

function initDataTable() {
    dataTable = $('#tablaUsuarios').DataTable({
        ajax: {
            url: API_URL,
            dataSrc: '', 
            error: function(xhr, error, thrown) {
                console.error("Detalle del error:", xhr.responseText);
                if (xhr.status === 403) {
                    Swal.fire('Acceso Denegado', 'Tu usuario no tiene rol de administrador en la base de datos.', 'error');
                } else if (xhr.status === 401) {
                    window.location.href = '/'; // Sesión expirada
                } else {
                    Swal.fire('Error', 'No se pudo cargar la tabla de usuarios.', 'error');
                }
            },
            beforeSend: function(xhr) {
                const token = localStorage.getItem('access_token');
                if (token) {
                    xhr.setRequestHeader('Authorization', 'Bearer ' + token);
                }
            }
        },
        columns: [
            { data: 'id' },
            { data: 'username' },
            { 
                data: 'rol',
                render: function(data) {
                    return data === 'admin' 
                        ? '<span class="badge bg-danger">Administrador</span>' 
                        : '<span class="badge bg-info text-dark">Analista</span>';
                }
            },
            { data: 'cedula' },
            { 
                data: 'estado',
                render: function(data) {
                    return data 
                        ? '<span class="badge bg-success">Activo</span>' 
                        : '<span class="badge bg-secondary">Inactivo</span>';
                }
            },
            {
                data: null,
                render: function(data, type, row) {
                    return `
                        <button class="btn btn-sm btn-warning me-1" onclick="editarUsuario(${row.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="eliminarUsuario(${row.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    `;
                }
            }
        ],
        language: {
            url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
        }
    });
}

// Abrir Modal para Crear
window.abrirModalUsuario = function() {
    document.getElementById('userForm').reset();
    document.getElementById('userId').value = '';
    document.getElementById('modalTitle').textContent = 'Nuevo Usuario';
    new bootstrap.Modal(document.getElementById('userModal')).show();
}

// Abrir Modal para Editar (Cargar datos)
window.editarUsuario = function(id) {
    // Buscar los datos en la tabla (DataTables tiene los datos en memoria)
    const data = dataTable.data().toArray().find(u => u.id === id);
    
    if (data) {
        document.getElementById('userId').value = data.id;
        document.getElementById('username').value = data.username;
        document.getElementById('rol').value = data.rol;
        document.getElementById('cedula').value = data.cedula || '';
        document.getElementById('estado').value = data.estado.toString().toLowerCase() === 'true' ? 'true' : 'false';
        
        document.getElementById('modalTitle').textContent = 'Editar Usuario';
        new bootstrap.Modal(document.getElementById('userModal')).show();
    }
}

// Guardar (Crear o Editar)
window.guardarUsuario = async function() {
    const id = document.getElementById('userId').value;
    const isEdit = !!id;
    
    const payload = {
        username: document.getElementById('username').value,
        rol: document.getElementById('rol').value,
        cedula: document.getElementById('cedula').value,
        estado: document.getElementById('estado').value === 'true'
    };

    // Solo enviamos password si se escribió algo (en edición) o siempre en creación
    const pass = document.getElementById('password').value;
    if (pass || !isEdit) {
        payload.password = pass;
    }

    const method = isEdit ? 'PUT' : 'POST';
    const url = isEdit ? `${API_URL}${id}/` : API_URL;

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                // Enviar Token si tu backend lo requiere (UsuarioCRUDView tiene csrf_exempt, pero quizás quieras validar rol)
                // 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') 
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            // Cerrar modal y recargar tabla
            const modalEl = document.getElementById('userModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();
            
            dataTable.ajax.reload(); // Recarga DataTables sin refrescar página
            Swal.fire('Éxito', 'Operación realizada correctamente', 'success');
        } else {
            Swal.fire('Error', result.error || 'Hubo un problema', 'error');
        }
    } catch (error) {
        console.error(error);
        Swal.fire('Error', 'Error de conexión', 'error');
    }
}

// Eliminar
window.eliminarUsuario = async function(id) {
    const confirm = await Swal.fire({
        title: '¿Estás seguro?',
        text: "No podrás revertir esto",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    });

    if (confirm.isConfirmed) {
        try {
            const response = await fetch(`${API_URL}${id}/`, {
                method: 'DELETE'
            });

            if (response.ok) {
                dataTable.ajax.reload();
                Swal.fire('Eliminado', 'El usuario ha sido eliminado.', 'success');
            } else {
                Swal.fire('Error', 'No se pudo eliminar', 'error');
            }
        } catch (error) {
            Swal.fire('Error', 'Error de conexión', 'error');
        }
    }
}