const AUTH_URL = `${window.location.origin}/auth`;

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('auth_token')) {
        window.location.href = '/app';
        return;
    }

    document.getElementById('email-form').addEventListener('submit', requestOtp);
    document.getElementById('otp-form').addEventListener('submit', verifyOtp);
    document.getElementById('back-btn').addEventListener('click', backToEmail);
});

function requestOtp(e) {
    e.preventDefault();
    const email = document.getElementById('email').value.trim();

    fetch(`${AUTH_URL}/request-otp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
    })
    .then(r => {
        if (!r.ok) return r.json().then(err => { throw new Error(err.detail || 'Error al enviar código'); });
        return r.json();
    })
    .then(() => {
        document.getElementById('email-form').style.display = 'none';
        document.getElementById('otp-form').style.display = 'block';
        document.getElementById('login-title').textContent = `Ingresa el código enviado a ${email}`;
        document.getElementById('code').focus();
        showMessage('Código enviado a tu correo', 'success');
    })
    .catch(err => showMessage('Error: ' + err.message, 'error'));
}

function verifyOtp(e) {
    if (e) e.preventDefault();
    const email = document.getElementById('email').value.trim();
    const code = document.getElementById('code').value.replace(/\s+/g, '');
    if (!code) {
        showMessage('Ingresa el código', 'error');
        return;
    }

    fetch(`${AUTH_URL}/verify-otp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, code })
    })
    .then(r => {
        if (!r.ok) return r.json().then(err => { throw new Error(err.detail || 'Código inválido'); });
        return r.json();
    })
    .then(data => {
        localStorage.setItem('auth_token', data.token);
        localStorage.setItem('auth_email', data.email);
        window.location.href = '/app';
    })
    .catch(err => showMessage('Error: ' + err.message, 'error'));
}

function backToEmail() {
    document.getElementById('otp-form').style.display = 'none';
    document.getElementById('email-form').style.display = 'block';
    document.getElementById('login-title').textContent = 'Ingresa tu correo';
    document.getElementById('code').value = '';
}

function showMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;

    const container = document.querySelector('.container');
    container.insertBefore(messageDiv, container.firstChild);

    setTimeout(() => { messageDiv.style.display = 'none'; }, 3000);
}
