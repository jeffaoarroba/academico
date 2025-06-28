import sqlite3


class BancoDados:
    def __init__(self, nome_banco='controle_academico.db'):
        self.nome_banco = nome_banco
        self.conexao = None
        self.cursor = None
        print("## BANCO DE DADOS")
        print("arquivo", nome_banco)

    def conectar(self):
        """Cria a conexao com o banco de dados"""
        self.conexao = sqlite3.connect(self.nome_banco)
        self.cursor = self.conexao.cursor()
        print("OK conectado")

    def desconectar(self):
        """Fecha a conexao com o banco de dados"""
        if self.conexao:
            self.conexao.commit()
            self.conexao.close()
            self.conexao = None
            self.cursor = None
            print("OK desconectado")

    def executar(self, sql):
        if not sql: return
        if not self.cursor:
            self.conectar()
        self.cursor.execute(sql)
        print("OK sql", sql)
        dados = self.cursor.fetchall()
        self.desconectar()
        return dados

    def criar_tabelas(self):
        """Criar as tabelas no banco de dados"""
        self.conectar()

        """cria a tabela disciplina, se nao existir"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS disciplina (
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                carga_horaria INTEGER NOT NULL,
                nome_professor TEXT NOT NULL
            )
        ''')
        print("OK tabela criada: disciplina")

        """cria a tabela aluno, se nao existir"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS aluno (
                    cpf INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    ano_nascimento INTEGER NOT NULL,
                    email TEXT NOT NULL,
                    endereco TEXT NOT NULL
                )
        ''')
        print("OK tabela criada: aluno")

        """cria a tabela matricula, se nao existir"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS matricula (
                codigo_disciplina INTEGER NOT NULL,
                cpf_aluno INTEGER NOT NULL,
                matriculado_em DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (codigo_disciplina, cpf_aluno)
            )            
        ''')
        print("OK tabela criada: matricula")

        self.desconectar()


if __name__ == '__main__':
    banco = BancoDados()
    banco.criar_tabelas()
