import sqlite3 as sql
conexao = sql.connect('Alunos.db')
cursor = conexao.cursor()

def criar_tabela():
    cursor.executer("""CREATE TABLE alunos(
    id INT, PRYMARU KEY, AUTO_INCREMENT,
    nome VARCHAR(50)
    )""");