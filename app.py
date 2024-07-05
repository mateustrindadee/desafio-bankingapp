from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_session import Session
import sqlite3
import hashlib
import os
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.urandom(24) 
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Conexão com o SQLite3
def init_db():
    if not os.path.exists('./instance'):
        os.makedirs('./instance')
    conn = sqlite3.connect('./instance/database.db')
    cursor = conn.cursor()
    
    # Tabela de cadastro dos usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            idUser INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            cpf VARCHAR(11) NOT NULL UNIQUE,
            cellphone VARCHAR(11) NOT NULL,
            date DATE NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            saldo DECIMAL NOT NULL
        )
    ''')
    
     # Tabela de transações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            idTransactions INTEGER PRIMARY KEY AUTOINCREMENT,
            destinUsercpf VARCHAR(11) NOT NULL,
            valor DECIMAL NOT NULL,
            dataTransf TEXT NOT NULL,
            FOREIGN KEY (idOrigin) REFERENCES users(idUser),
            FOREIGN KEY (destinUsercpf) REFERENCES users(cpf)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota de cadastro
@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form['name']
        cpf = request.form['cpf']
        cellphone = request.form['cellphone']
        date = request.form['date']
        email = request.form['email']
        password = request.form['password']
        
        # Verifica se o CPF ou email já está cadastrado
        conn = sqlite3.connect('./instance/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE cpf = ? OR email = ?', (cpf, email))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Já tem alguém cadastrado com essas credenciais!', 'error')
            return redirect(url_for('index'))
        
        # Hash da senha
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Saldo inicial da conta
        saldo_inicial = 0.0 
        
        # Inserir usuário no banco de dados
        cursor.execute('''
            INSERT INTO users (name, cpf, cellphone, date, email, password, saldo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, cpf, cellphone, date, email, hashed_password, saldo_inicial))
        conn.commit()
        print('\nCadastro realizado com sucesso!\n', 'success')
    except sqlite3.IntegrityError:
        print('\nJá existe um usuário com este CPF ou email!\n', 'error')
    except Exception as e:
        print(f'\nOcorreu um erro: {str(e)}\n', 'error')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('index'))

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    conn = sqlite3.connect('./instance/database.db')
    cursor = conn.cursor()
    
    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hashed_password))
        user = cursor.fetchone()
    except Exception as e:
        flash(f'Ocorreu um erro: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        cursor.close()
        conn.close()
    
    if user:
        session['idUser'] = user[0]
        print(f'O {email} logou!')
        return render_template('conta.html')
    else:
        print(f'Login falhou')
        return jsonify({'message': 'Login Credenciais inválidas'}), 401


@app.route('/dados_conta', methods=['GET'])
def dados_conta():
    try:
        # Obter idUser dos argumentos de consulta
        idUser = session.get('idUser')
        
        if not idUser:
            return jsonify({'message': 'Usuário não está logado'}), 401

        conn = sqlite3.connect('./instance/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, cpf, saldo FROM users WHERE idUser = ?', (idUser,))
        dados = cursor.fetchone()
        conn.close()

        if dados:
            dados_json = {
                'name': dados[0],
                'cpf': dados[1],
                'saldo': float(dados[2])  
            }
            return jsonify(dados_json), 200  
        else:
            return jsonify({'message': 'Nenhum usuário encontrado'}), 404  
    except Exception as e:
        return jsonify({'error': str(e)}), 500 



# Retorna o erro no front-end
@app.route('/processar-dados', methods=['POST'])
def processar_dados():
    dados = request.get_json()
    if 'nome' not in dados:
        return jsonify({'erro': 'Nome não foi fornecido'}), 400 
    return jsonify({'mensagem': 'Dados processados com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
