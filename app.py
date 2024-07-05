from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Para uso com mensagens flash

# Conexão com o SQLite3
def init_db():
    if not os.path.exists('./instance'):
        os.makedirs('./instance')
    conn = sqlite3.connect('./instance/database.db')
    cursor = conn.cursor()
    
    # Tabela de cadastro dos usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            cpf VARCHAR(11) NOT NULL,
            cellphone VARCHAR(11) NOT NULL,
            date DATE NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form['name']
        cpf = request.form['cpf']
        cellphone = request.form['cellphone']
        date = request.form['date']
        email = request.form['email']
        password = request.form['password']
        
        # Conectar ao banco de dados
        conn = sqlite3.connect('./instance/database.db')
        cursor = conn.cursor()
        
        # Hash da senha
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Inserir usuário no banco de dados
        cursor.execute('''
            INSERT INTO users (name, cpf, cellphone, date, email, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, cpf, cellphone, date, email, hashed_password))
        conn.commit()
        conn.close()
        
        print('Cadastro realizado com sucesso!', 'success')
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed: users.email' in str(e):
            print(f'Este email já está cadastrado. Por favor, use outro email.')
        else:
            print(f'Ocorreu um erro: {str(e)}')

    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    conn = sqlite3.connect('./instance/database.db')
    cursor = conn.cursor()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hashed_password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return redirect('https://stackoverflow.com/')
    else:
        return 'Login falhou'

if __name__ == '__main__':
    app.run(debug=True)


# def register_user(username, password):
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()
#     cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
#     conn.commit()
#     print(f'Usuário {username} registrado com sucesso.')


# def authenticate_user(username, password):
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()
#     cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
#     return cursor.fetchone() is not None









































# def main():
#     while True:
#         print('\nEscolha uma opção:')
#         print('1. Registrar')
#         print('2. Entrar')
#         print('3. Sair')

#         opcao = input('Opção: ')

#         if opcao == '1':
#             username = input('Digite o nome de usuário: ')
#             password = input('Digite a senha: ')
#             register_user(username, password)

#         elif opcao == '2':
#             username = input('Digite o nome de usuário: ')
#             password = input('Digite a senha: ')
#             if authenticate_user(username, password):
#                 print(f'Usuário {username} autenticado com sucesso!')
#             else:
#                 print('Falha na autenticação. Usuário ou senha incorretos.')

#         elif opcao == '3':
#             print('Saindo...')
#             break

#         else:
#             print('Opção inválida. Tente novamente.')

# if __name__ == '__main__':
#     main()


# conn.close()










# outro
    # Tabelas do banco de dados
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name VARCHAR(50) NOT NULL,
#         cpf VARCHAR(11) NOT NULL,
#         cellphone VARCHAR(11) NOT NULL,
#         date VARCHAR(8)
#         email VARCHAR(100) NOT NULL,
#         password VARCHAR(100) NOT NULL
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS accounts(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         number TEXT NOT NULL,
#         balance REAL NOT NULL,
#         user_id INTEGER NOT NULL,
#         FOREIGN KEY (user_id) REFERENCES users(id)                       
#     )
# ''')
    
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS transactions (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         origin_id INTEGER NOT NULL,
#         destination_id INTEGER NOT NULL,
#         valor REAL NOT NULL,
#         data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         FOREING KEY (origin_id) REFERENCES accounts(id),
#         FOREING KEY (destination_id) REFERENCES accounts(id)              
#     )          
# ''')

# conn.commit()

# def create_user(name, cpf, celular, date, email, password):
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()
#     cursor.execute('INSERT INTO users (name, cpf, cellphone, date, email, password) VALUES (?. ?)', (name, hashed_password))
#     conn.commit()
#     print(f'Usuário {name} criado com sucesso.')

