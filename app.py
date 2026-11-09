import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__)

# Chave usada para proteger o cookie de sessão (é ele que lembra quem está logado).
# Em produção, defina a variável de ambiente SECRET_KEY com um valor secreto.
app.secret_key = os.environ.get("SECRET_KEY", "chave-de-desenvolvimento")

# Caminho do banco, sempre na mesma pasta deste arquivo
BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Alunos.db")


# ===================== Banco de dados (CRUD) =====================

def conectar():
    # Cada função abre e fecha a própria conexão, porque o Flask
    # atende as requisições em threads diferentes.
    conexao = sqlite3.connect(BANCO)
    conexao.row_factory = sqlite3.Row  # permite usar aluno["nome"]
    return conexao


def criar_tabela():
    conexao = conectar()
    conexao.execute("""CREATE TABLE IF NOT EXISTS alunos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(50),
        rm INT UNIQUE
    )""")
    conexao.commit()
    conexao.close()


# CREATE
def inserir_aluno(rm, nome):
    """Cadastra o aluno. Retorna False se o RM já estiver cadastrado."""
    conexao = conectar()
    try:
        conexao.execute("INSERT INTO alunos (rm, nome) VALUES (?, ?)", (rm, nome))
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conexao.close()


# READ
def buscar_aluno(rm):
    """Retorna o aluno com esse RM, ou None se não existir."""
    conexao = conectar()
    aluno = conexao.execute(
        "SELECT id, nome, rm FROM alunos WHERE rm = ?", (rm,)
    ).fetchone()
    conexao.close()
    return aluno


# UPDATE
def atualizar_nome(rm, nome):
    conexao = conectar()
    conexao.execute("UPDATE alunos SET nome = ? WHERE rm = ?", (nome, rm))
    conexao.commit()
    conexao.close()


# DELETE
def deletar_aluno(rm):
    conexao = conectar()
    conexao.execute("DELETE FROM alunos WHERE rm = ?", (rm,))
    conexao.commit()
    conexao.close()


# ===================== Funções auxiliares =====================

def ler_rm(texto):
    """Converte o RM digitado em número. Retorna None se for inválido."""
    try:
        rm = int(texto)
    except (TypeError, ValueError):
        return None
    # RM precisa ser positivo e ter no máximo 10 dígitos
    if 0 < rm < 10**10:
        return rm
    return None


def ler_nome(texto):
    return (texto or "").strip().title()


def nome_valido(nome):
    # O SQLite não respeita o limite do VARCHAR(50), então conferimos aqui
    return 0 < len(nome) <= 50


def aluno_logado():
    """Retorna o aluno que está logado, ou None se ninguém estiver."""
    rm = session.get("rm")
    if rm is None:
        return None
    aluno = buscar_aluno(rm)
    if aluno is None:
        # A conta foi apagada por fora (ex.: pelo main.py), então desloga
        session.clear()
    return aluno


# ===================== Páginas =====================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/integrantes")
def integrantes():
    return render_template("integrantes.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")

    rm_digitado = request.form.get("rm", "")
    nome = ler_nome(request.form.get("nome"))
    rm = ler_rm(rm_digitado)

    if not nome_valido(nome):
        flash("Digite um nome de 1 a 50 caracteres.", "erro")
    elif rm is None:
        flash("RM inválido. Digite apenas números.", "erro")
    elif not inserir_aluno(rm, nome):
        flash("Esse RM já está cadastrado.", "erro")
    else:
        session["rm"] = rm
        flash("Conta criada com sucesso!", "sucesso")
        return redirect("/perfil")

    # Deu erro: mostra o formulário de novo com o que a pessoa digitou
    return render_template("cadastro.html", nome=nome, rm=rm_digitado)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if aluno_logado():
            return redirect("/perfil")
        return render_template("login.html")

    rm_digitado = request.form.get("rm", "")
    rm = ler_rm(rm_digitado)

    if rm is None:
        flash("RM inválido. Digite apenas números.", "erro")
        return render_template("login.html", rm=rm_digitado)

    aluno = buscar_aluno(rm)
    if aluno is None:
        flash("RM não encontrado.", "erro")
        return render_template("login.html", rm=rm_digitado)

    session["rm"] = aluno["rm"]
    flash(f"Olá, {aluno['nome']}!", "sucesso")
    return redirect("/perfil")


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "sucesso")
    return redirect("/")


@app.route("/perfil")
def perfil():
    aluno = aluno_logado()
    if aluno is None:
        flash("Faça login para acessar sua conta.", "erro")
        return redirect("/login")
    return render_template("perfil.html", aluno=aluno)


@app.route("/perfil/editar", methods=["POST"])
def editar():
    aluno = aluno_logado()
    if aluno is None:
        flash("Faça login para acessar sua conta.", "erro")
        return redirect("/login")

    nome = ler_nome(request.form.get("nome"))
    if not nome_valido(nome):
        flash("Digite um nome de 1 a 50 caracteres.", "erro")
    else:
        atualizar_nome(aluno["rm"], nome)
        flash("Nome atualizado!", "sucesso")
    return redirect("/perfil")


@app.route("/perfil/deletar", methods=["POST"])
def deletar():
    aluno = aluno_logado()
    if aluno is None:
        flash("Faça login para acessar sua conta.", "erro")
        return redirect("/login")

    deletar_aluno(aluno["rm"])
    session.clear()
    flash("Conta excluída.", "sucesso")
    return redirect("/")


criar_tabela()

if __name__ == "__main__":
    app.run(debug=True)
