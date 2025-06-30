import sqlite3


class BancoDados:
    def __init__(self, nome_banco='controle_academico.db'):
        self.nome_banco = nome_banco
        self.conexao = None
        self.cursor = None
        print("BANCO DADOS arquivo", nome_banco)

    def conectar(self):
        """Cria a conexao com o banco de dados"""
        if not self.conexao:
            self.conexao = sqlite3.connect(self.nome_banco)
            # para cursor.fetchall retornar as colunas do sql
            self.conexao.row_factory = sqlite3.Row
        self.cursor = self.conexao.cursor()
        print("BANCO DADOS conectado")

    def desconectar(self):
        """Fecha a conexao com o banco de dados"""
        if self.conexao:
            self.conexao.commit()
            self.conexao.close()
            self.conexao = None
            self.cursor = None
            print("BANCO DADOS desconectado")

    def confirmar(self):
        if self.conexao:
            self.conexao.commit()

    def executar(self, sql, parametros=None):
        if not sql: return
        if not self.cursor:
            self.conectar()
        if not parametros:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, parametros)
        print("BANCO DADOS sql", sql)
        dados = self.cursor.fetchall()
        self.desconectar()
        lista = []
        for registro in dados:
            item = dict(registro)
            lista.append(item)
        return lista

    def select(self, select, parametros=None):
        dados = self.executar(select, parametros)
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
        print("BANCO DADOS tabela: disciplina")

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
        print("BANCO DADOS tabela: aluno")

        """cria a tabela matricula, se nao existir"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS matricula (
                codigo_disciplina INTEGER NOT NULL,
                cpf_aluno INTEGER NOT NULL,
                matriculado_em DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (codigo_disciplina, cpf_aluno)
            )            
        ''')
        print("BANCO DADOS tabela: matricula")

        self.desconectar()


if __name__ == '__main__':
    banco = BancoDados()
    banco.criar_tabelas()
