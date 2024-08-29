import sqlite3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('escola.db')
    conn.row_factory = sqlite3.Row
    return conn

# Função para criar as tabelas
def create_tables():
    conn = get_db_connection()
    
    # Cria a tabela de turmas
    conn.execute('''
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')
    
    # Cria a tabela de alunos
    conn.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            turma_id INTEGER,
            FOREIGN KEY (turma_id) REFERENCES turmas (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Chama a função para criar as tabelas
create_tables()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Cadastra uma nova turma
        if 'nome_turma' in request.form:
            nome_turma = request.form['nome_turma']
            conn = get_db_connection()
            conn.execute('INSERT INTO turmas (nome) VALUES (?)', (nome_turma,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
        # Cadastra um novo aluno
        elif 'nome_aluno' in request.form:
            nome_aluno = request.form['nome_aluno']
            idade = request.form.get('idade', None)
            turma_id = request.form.get('turma_id', None)

            if turma_id:
                conn = get_db_connection()
                conn.execute('''
                    INSERT INTO alunos (nome, idade, turma_id)
                    VALUES (?, ?, ?)
                ''', (nome_aluno, idade, turma_id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))

    # Busca as turmas e alunos cadastrados
    conn = get_db_connection()
    turmas = conn.execute('SELECT * FROM turmas').fetchall()
    alunos = conn.execute('''
        SELECT alunos.*, turmas.nome AS turma_nome
        FROM alunos
        JOIN turmas ON alunos.turma_id = turmas.id
    ''').fetchall()
    conn.close()

    return render_template('index.html', turmas=turmas, alunos=alunos)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_aluno(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM alunos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_aluno(id):
    conn = get_db_connection()

    if request.method == 'POST':
        nome_aluno = request.form['nome_aluno']
        idade = request.form.get('idade', None)
        turma_id = request.form.get('turma_id', None)

        conn.execute('''
            UPDATE alunos
            SET nome = ?, idade = ?, turma_id = ?
            WHERE id = ?
        ''', (nome_aluno, idade, turma_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    else:
        aluno = conn.execute('SELECT * FROM alunos WHERE id = ?', (id,)).fetchone()
        turmas = conn.execute('SELECT * FROM turmas').fetchall()
        conn.close()
        return render_template('edit.html', aluno=aluno, turmas=turmas)

if __name__ == '__main__':
    app.run(debug=True)