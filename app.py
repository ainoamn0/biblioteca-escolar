from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        usuario = request.form.get('usuario')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if not all([nome, sobrenome, usuario, email, senha]):
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('cadastro'))

        hashed_password = generate_password_hash(senha)
        
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO usuarios (nome, sobrenome, usuario, email, senha) VALUES (?, ?, ?, ?, ?)',
                         (nome, sobrenome, usuario, email, hashed_password))
            conn.commit()
            conn.close()
            flash('Cadastro realizado com sucesso! Faça login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Usuário ou E-mail já cadastrados.')
            return redirect(url_for('cadastro'))
            
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['senha'], senha):
            session['user_id'] = user['id']
            session['user_name'] = user['nome']
            return redirect(url_for('dashboard'))
        else:
            flash('E-mail ou senha incorretos.')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página.')
        return redirect(url_for('login'))
    
    return render_template('interface.html', user_name=session.get('user_name'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.')
    return redirect(url_for('index'))

@app.route('/consultarapida')
def consultarapida():
    if 'user_id' not in session:
        flash('Faça login para acessar o acervo da biblioteca.')
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '')
    
    conn = get_db_connection()
    if search_query:
        books = conn.execute('''
            SELECT * FROM livros 
            WHERE titulo LIKE ? OR autor LIKE ? OR categoria LIKE ?
        ''', (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')).fetchall()
    else:
        books = conn.execute('SELECT * FROM livros').fetchall()
    conn.close()
    
    return render_template('consultarapida.html', books=books, search_query=search_query)

@app.route('/suporte')
def suporte():
    return render_template('suporte.html')

if __name__ == '__main__':
    app.run(debug=True)
