const API_URL = `${window.location.origin}/students`;

function getToken() {
    return localStorage.getItem('auth_token');
}

function authHeaders(extra = {}) {
    const token = getToken();
    return token ? { ...extra, 'Authorization': `Bearer ${token}` } : extra;
}

function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_email');
    window.location.href = '/';
}

function handleAuth(response) {
    if (response.status === 401) {
        logout();
        throw new Error('Sesión expirada');
    }
    return response;
}

document.addEventListener('DOMContentLoaded', () => {
    if (!getToken()) {
        window.location.href = '/';
        return;
    }
    const email = localStorage.getItem('auth_email');
    const userEl = document.getElementById('user-email');
    if (userEl && email) userEl.textContent = email;
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) logoutBtn.addEventListener('click', logout);

    loadStudents();
    setupForm();
});

function loadStudents() {
    fetch(API_URL, { headers: authHeaders() })
        .then(handleAuth)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar estudiantes');
            }
            return response.json();
        })
        .then(students => {
            renderStudents(students);
        })
        .catch(error => {
            showMessage('Error al cargar estudiantes: ' + error.message, 'error');
        });
}

function renderStudents(students) {
    const tbody = document.getElementById('students-list');
    tbody.innerHTML = '';

    if (students.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No hay estudiantes</td></tr>';
        return;
    }

    students.forEach(student => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${student.id}</td>
            <td>${student.name}</td>
            <td>${student.age}</td>
            <td>${student.grade}</td>
            <td>
                <button class="action-btn btn-edit" onclick="editStudent(${student.id}, '${student.name}', ${student.age}, ${student.grade})">Editar</button>
                <button class="action-btn btn-delete" onclick="deleteStudent(${student.id})">Eliminar</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function setupForm() {
    const form = document.getElementById('student-form');
    const cancelBtn = document.getElementById('cancel-btn');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        saveStudent();
    });

    cancelBtn.addEventListener('click', resetForm);
}

function saveStudent() {
    const id = document.getElementById('student-id').value;
    const name = document.getElementById('name').value;
    const age = parseInt(document.getElementById('age').value);
    const grade = parseFloat(document.getElementById('grade').value);

    const studentData = { name, age, grade };

    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_URL}/${id}` : API_URL;

    fetch(url, {
        method: method,
        headers: authHeaders({ 'Content-Type': 'application/json' }),
        body: JSON.stringify(studentData)
    })
    .then(handleAuth)
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.detail || 'Error en la operación'); });
        }
        return response.json();
    })
    .then(data => {
        showMessage(id ? 'Estudiante actualizado' : 'Estudiante creado', 'success');
        resetForm();
        loadStudents();
    })
    .catch(error => {
        showMessage('Error: ' + error.message, 'error');
    });
}

function editStudent(id, name, age, grade) {
    document.getElementById('student-id').value = id;
    document.getElementById('name').value = name;
    document.getElementById('age').value = age;
    document.getElementById('grade').value = grade;
    document.getElementById('form-title').textContent = 'Editar Estudiante';
    document.getElementById('submit-btn').textContent = 'Actualizar';
    document.getElementById('cancel-btn').style.display = 'inline-block';
}

function deleteStudent(id) {
    if (!confirm('¿Estás seguro de eliminar este estudiante?')) {
        return;
    }

    fetch(`${API_URL}/${id}`, {
        method: 'DELETE',
        headers: authHeaders()
    })
    .then(handleAuth)
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.detail || 'Error al eliminar'); });
        }
        return response.json();
    })
    .then(data => {
        showMessage('Estudiante eliminado', 'success');
        loadStudents();
    })
    .catch(error => {
        showMessage('Error: ' + error.message, 'error');
    });
}

function resetForm() {
    document.getElementById('student-form').reset();
    document.getElementById('student-id').value = '';
    document.getElementById('form-title').textContent = 'Nuevo Estudiante';
    document.getElementById('submit-btn').textContent = 'Guardar';
    document.getElementById('cancel-btn').style.display = 'none';
}

function showMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;

    const container = document.querySelector('.container');
    container.insertBefore(messageDiv, container.firstChild);

    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 3000);
}
