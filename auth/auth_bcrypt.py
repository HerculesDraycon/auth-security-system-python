import sqlite3
import bcrypt
#Conexao com o bd.
def conectar():
    return sqlite3.connect("users.db")
#Registro de ususario com os dados, agora com hash e salt aplicados na senha.
def registrar(username, password):
    conn = conectar()
    cursor = conn.cursor()
    #Utilizacao do bcrypt
    senha_bytes = password.encode()
    senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())

    try:
        cursor.execute("""
        INSERT INTO usuarios (username, password)
        VALUES (?, ?)
        """, (username, senha_hash))
        #Entrega dos dados pela conexao e notificacao de sucesso.
        conn.commit()
        print("Usuário cadastrado com sucesso!")
        #Demonstracao
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
    SELECT password FROM usuarios
    WHERE username=?
    """, (username,))

    result = cursor.fetchone()
    conn.close()
    #Trata o caso de que se o ususario nao estiver no bd, o sistema notifica.
    if result is None:
        print("Usuário não encontrado!")
        return False

    senha_hash = result[0]
    #Se a senha for compativel, ok, se nao, erro notificado.
    if bcrypt.checkpw(password.encode(), senha_hash):
        print("Login OK")
        return True
    else:
        print("Senha incorreta!")
        return False


# MENU DE TESTE

def menu():
    while True:
        print("\n=== SISTEMA DE LOGIN (BCRYPT - SEGURO) ===")
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