// Função para abrir o modal 
function mostrarModal() {
    document.getElementById('modalBg').style.display = 'flex';
}

// Função para fechar o modal
function fecharModal() {
    document.getElementById('modalBg').style.display = 'none';
}

// Função para validar as senhas
function validatePassword() {
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        alert("As senhas não coincidem.");
        return false;
    }
    return true;
}
