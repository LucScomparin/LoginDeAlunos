import sqlite3 as sql

conexao = sql.connect('Alunos.db')
cursor = conexao.cursor()


def criar_tabela():
    cursor.execute("""CREATE TABLE IF NOT EXISTS alunos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50),
    rm INT UNIQUE
    )""")
    conexao.commit()

3
def ler_rm():
    while True:
        try:
            return int(input("Digite seu RM:\n"))
        except ValueError:
            print("RM inválido. Digite apenas números.")


def inserir_aluno(rm, nome):
    cursor.execute("INSERT INTO alunos (rm, nome) VALUES (?, ?)", (rm, nome))
    conexao.commit()


def criar_conta():
    rm = ler_rm()
    nome = input("Digite seu nome\n").strip().title()
    try:
        inserir_aluno(rm, nome)
        print("CONTA CRIADA")
    except sql.IntegrityError:
        print("Esse RM já está cadastrado.")


def login():
    rm = ler_rm()
    cursor.execute("SELECT nome FROM alunos WHERE rm = ?", (rm,))
    aluno = cursor.fetchone()

    if aluno:
        print(f"OLAAAA, {aluno[0]}!")
        return True
    else:
        print("RM não encontrado.")
        return False


def deletar():
    rm = ler_rm()
    cursor.execute("DELETE FROM alunos WHERE rm = ?", (rm,))
    conexao.commit()
    if cursor.rowcount > 0:
        print("CONTA DELETADA")
    else:
        print("RM não encontrado.")


def menu():
    print("Olá, seja bem vindo ao software de login de alunos!")
    while True:
        resposta_menu = input(
            "\nDigite .criar para criar uma conta, .deletar para deletar uma conta, "
            ".exit para sair, ou apenas Enter para fazer login.\n"
        ).lower().strip()
        if resposta_menu == ".exit":
            print("Obrigado por usar nosso software.")
            break
        elif resposta_menu == ".criar":
            criar_conta()
        elif resposta_menu == ".deletar":
            deletar()
        elif resposta_menu == "":
            login()
        else:
            print("Opção inválida.")


criar_tabela()
menu()
conexao.close()


