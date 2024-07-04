from flask import Flask, render_template, request, redirect, url_for # type: ignore
import sqlite3
import hashlib
import string

app = Flask(__name__)

# Conexão com o SQLite3
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            cpf VARCHAR(11) NOT NULL,
            cellphone VARCHAR(11) NOT NULL,
            date VARCHAR(8),
            email VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    ''')
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
    conn.commit()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    cpf = request.form['cpf']
    cellphone = request.form['cellphone']
    date = request.form['date']
    email = request.form['email']
    password = request.form['password']


    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('INSERT INTO users (name, cpf, cellphone, date, email, password) VALUES (?. ?)', (name, hashed_password))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

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

