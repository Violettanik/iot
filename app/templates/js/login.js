document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.querySelector('.log__btn');

    // Переключение видимости пароля
    $('#toggle-password').on('click', function () {
        let passwordInput = $('#log-password-input');
        if (passwordInput.attr('type') === 'password') {
            passwordInput.attr('type', 'text');
            $(this).text('visibility_off');
        } else {
            passwordInput.attr('type', 'password');
            $(this).text('visibility'); 
        }
    });
    
    loginButton.addEventListener('click', async function() {
        const loginInput = document.getElementById('log-login-input').value;
        const passwordInput = document.getElementById('log-password-input').value;

//        const response = await fetch('https://iotdatahub.online/iot_lk/login/', {
        const response = await fetch('http://127.0.0.1:5000/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + btoa(`${loginInput}:${passwordInput}`)
            }
        });

        const result = await response.json();

        if (response.ok) {
            localStorage.setItem('token', result.token);
            window.location.href = 'main.html';
        } else {
            alert('Ошибка: ' + result.error);
        }
    });
});
