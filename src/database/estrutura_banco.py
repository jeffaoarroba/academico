# crie uma conexao com o banco de dados SQLite e crie as tabelas necessárias
import sqlite3

# INTEGER: para números inteiros.
# TEXT: para texto.
# NOT NULL: para campo obrigatorio.          

def criar_conexao():
    conexao = sqlite3.connect('controle_academico.db')
    return conexao

def criar_tabelas():
    conexao = criar_conexao()
    db = conexao.cursor()

    # tabela de disciplina
    db.execute('''
        CREATE TABLE IF NOT EXISTS disciplina (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            carga_horaria INTEGER NOT NULL,
            nome_professor TEXT NOT NULL
        )
    ''')

    # tabela de aluno
    db.execute('''
        CREATE TABLE IF NOT EXISTS aluno (
            cpf INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            data_nascimento DATE NOT NULL,
            email TEXT NOT NULL,
            endereco TEXT NOT NULL
        )
    ''')

    # Criar tabela de matrícula
    db.execute('''
        CREATE TABLE IF NOT EXISTS matricula (
            codigo_disciplina INTEGER NOT NULL,
            cpf_aluno INTEGER NOT NULL,
            matriculado_em DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (codigo_disciplina, cpf_aluno)
        )
    ''')

    conexao.commit()
    conexao.close()


criar_tabelas()

"""
DML - Data Manipulation Language
C reate | INSERT INTO x
R read | SELECT * FROM x
U update | UPDATE x SET nome=123 WHERE codigo=1
D elete | DELETE FROM x WHERE codigo=1


DDL - Data Definition Language
CREATE TABLE
DROP TABLE
CREATE FUNCTION
CREATE PROCEDURE
CREATE VIEW
DROP TABLE
DROP VIEW
DROP PROCEDURE
ALTER TABLE
ALTER PROCEDURE
"""