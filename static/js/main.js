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

// Função pra puxar os dados da conta logada
function buscarDadosConta(){
    fetch('/dados_conta')
        .then(response => response.json())
        .then(data => {
            document.getElementById('name').innerText = data.name;
            document.getElementById('cpf').innerText = data.cpf;
            document.getElementById('saldo').innerText = data.saldo;
        })
        .catch(error => {
            console.error('Erro ao buscar dados da conta:', error)
        });
}
// Chama a função pra buscar os dados assim que a página carrega
window.onload = buscarDadosConta;

// Função pra revelar a área de transação
function revelarTransferencia(){
    document.getElementById('transferencia').style.display = "block";
}

//
fetch('/processar-dados', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ nome: 'valor' })  // Exemplo de dados a serem enviados
})
.then(response => {
    if (!response.ok) {
        throw new Error('Erro ao processar dados');
    }
    return response.json();
})
.then(data => {
    console.log('Dados processados com sucesso:', data);
})
.catch(error => {
    console.error('Erro:', error.message);
    alert('Ocorreu um erro ao processar os dados. Por favor, tente novamente mais tarde.');
});


