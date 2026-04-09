import sqlite3
#Conexao com bd.
def conectar():
    return sqlite3.connect("users.db")
#Registro de ususario com os dados, sem nenhuma camda de seguranca aplicada.
def registrar(username, password):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO usuarios (username, password)
        VALUES (?, ?)
        """, (username, password))
        #Entrega dos dados pela conexao e notificacao de sucesso.
        conn.commit()
        print("Usuário cadastrado com sucesso!")
    #Adicionada a excessao de que um ususario duplicado ja existe, retorna erro.
    except sqlite3.IntegrityError:
        print("Erro: usuário já existe!")

    finally:
        conn.close()
#Funcao de login com os dados fornecidos do usuario.
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

    senha_bd = result[0]
    #Se a senha for compativel, ok, se nao, erro notificado.
    if senha_bd == password:
        print("Login OK")
        return True
    else:
        print("Senha incorreta!")
        return False


# MENU DE TESTE

def menu():
    while True:
        print("\n=== SISTEMA DE LOGIN (PLAIN TEXT - INSEGURO) ===")
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