// Função para abrir o model 
function mostrarModal(){
    document.getElementById('modalBg').style.display = 'flex';
}

// Função para fechar o model
function fecharModal(){
    document.getElementById('modalBg').style.display = 'none';
}


function validatePassword(){
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;

    if(password != confirmPassword){
        alert("As senhas não coincidem.");
        return false;
    }
    return false;
}