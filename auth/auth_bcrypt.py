import sqlite3
import bcrypt
from auth.utils import validar_forca_senha, checar_bloqueio, registrar_tentativa_falha, resetar_tentativas
#Conexao com o bd.
def conectar():
    return sqlite3.connect("users.db")
#Registro de ususario com os dados, agora com hash e salt aplicados na senha.
def registrar(username, password):
    # Validacao introduzida para nao permitir senhas com baixa complexidade (Melhoria 2).
    valida, msg = validar_forca_senha(password)
    if not valida:
        print(f"Erro: {msg}")
        return

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

    # Previne que contas sendo atacadas por forca bruta sejam sequer roteadas ao banco (Melhoria 1).
    bloqueado, msg = checar_bloqueio(cursor, username)
    if bloqueado:
        print(msg)
        conn.close()
        return False

    cursor.execute("""
    SELECT password FROM usuarios
    WHERE username=?
    """, (username,))

    result = cursor.fetchone()
    #Trata o caso de que se o ususario nao estiver no bd, o sistema notifica.
    if result is None:
        print("Usuário não encontrado!")
        conn.close()
        return False

    senha_hash = result[0]
    #Se a senha for compativel, ok, se nao, erro notificado.
    if bcrypt.checkpw(password.encode(), senha_hash):
        # Reseta os contadores de erro na conta para limpar o status dela.
        resetar_tentativas(cursor, conn, username)
        print("Login OK")
        conn.close()
        return True
    else:
        # Incrementa +1 erro no contador e trava temporariamente a conta no 3o erro.
        registrar_tentativa_falha(cursor, conn, username)
        conn.close()
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