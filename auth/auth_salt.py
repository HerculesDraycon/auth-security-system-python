import sqlite3
import hashlib
import os
#Conexao com o bd.
def conectar():
    return sqlite3.connect("users.db")
#Geracao de salt para juncao nas senhas.
def gerar_salt():
    return os.urandom(16).hex()
#Aplicacao de hash_md5 na senha fornecida com sha256.
def hash_senha(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()
#Registro de ususario com os dados, agora com hash e salt aplicados na senha.
def registrar(username, password):
    conn = conectar()
    cursor = conn.cursor()

    salt = gerar_salt()
    senha_hash = hash_senha(password, salt)

    try:
        cursor.execute("""
        INSERT INTO usuarios (username, password, salt)
        VALUES (?, ?, ?)
        """, (username, senha_hash, salt))
        #Entrega dos dados pela conexao e notificacao de sucesso.
        conn.commit()
        print("Usuário cadastrado com sucesso!")
        #Demonstracao do salt gerado + hash
        print(f"Salt usado: {salt}")
        print(f"Hash gerado: {senha_hash}")
    #Adicionada a excessao de que um ususario duplicado ja existe, retorna erro.
    except sqlite3.IntegrityError:
        print("Erro: usuário já existe!")

    finally:
        conn.close()
#Funcao de login com os dados fornecidos do usuario(senha em seu modo padrao). 
def login(username, password):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT password, salt FROM usuarios
    WHERE username=?
    """, (username,))

    result = cursor.fetchone()

    conn.close()
    #Trata o caso de que se o ususario nao estiver no bd, o sistema notifica.
    if result is None:
        print("Usuário não encontrado!")
        return False

    senha_bd, salt = result
    senha_hash = hash_senha(password, salt)
    #Se a senha for compativel, ok, se nao, erro notificado.
    if senha_hash == senha_bd:
        print("Login OK")
        return True
    else:
        print("Senha incorreta!")
        return False


# MENU DE TESTE

def menu():
    while True:
        print("\n=== SISTEMA DE LOGIN (HASH + SALT) ===")
        print("1 - Registrar")
        print("2 - Login")
        print("3 - Sair")
        #Variavel de controle da escolha do usuario na interface.
        op = input("Escolha: ")

        if op == "1":
            user = input("Usuário: ")
            senha = input("Senha: ")
            registrar(user, senha)

        elif op == "2":
            user = input("Usuário: ")
            senha = input("Senha: ")
            login(user, senha)

        elif op == "3":
            break

        else:
            print("Opção inválida!")

#Correspondencia com main.py.
if __name__ == "__main__":
    menu()