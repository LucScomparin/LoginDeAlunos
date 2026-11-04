import sqlite3 as sql
conexao = sql.connect('Alunos.db')
cursor = conexao.cursor()
def CriarConta():
    rm = int(input("Digite seu RM:\n"))
    nome = input("Digite seu nome").strip().title()
    inserir_aluno(rm,nome)
def criar_tabela():
    cursor.execute("""CREATE TABLE IF NOT EXISTS alunos(
    id INT PRYMARY KEY AUTO_INCREMENT NOT NULL,
    nome VARCHAR(50),
    rm INT UNIQUE 
    )""");
    conexao.commit()
def login():
    rm = int(input("Digite seu RM:\n"))
    cursor.execute("""SELECT rm FROM Alunos """)
    rm_de_alunos = cursor.fetchall()
    for rms in rm_de_alunos:
        print(rms)
        print(rm)
        if rms == rm:
            print("OLAAAA!")
        else:
            print("erro")
            break

def deletar(rm):
    cursor.execute("""DELETE FROM Alunos
    WHERE id = (?),"""(rm))
    conexao.commit()
    print("CONTA DELETADA")


def inserir_aluno(rm, nome):
    cursor.execute("INSERT INTO alunos (rm, nome) VALUES (?, ?)", (rm, nome))
    conexao.commit()
def menu():
    while True:
        print("Olá, seja bem vindo ao software de login de alunos!")
        resposta_menu = input("Para sair digite .exit, caso não tenha uma conta digite .login, para continuar digite Enter. \n")
        if resposta_menu.lower().strip() == ".exit":
            print("Obrigado por usar nosso software.")
            break
        elif resposta_menu.lower().strip() == ".login":
            criar_tabela()
            CriarConta()
        elif resposta_menu.lower().strip() == "":
            login()

menu()