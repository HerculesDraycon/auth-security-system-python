import sqlite3
import bcrypt
import pyotp

def conectar():
    return sqlite3.connect("users.db")


def registrar(username, password):
    conn = conectar()
    cursor = conn.cursor()

    senha_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Gera o segredo 2FA
    otp_secret = pyotp.random_base32()

    try:
        cursor.execute("""
        INSERT INTO usuarios (username, password, otp_secret)
        VALUES (?, ?, ?)
        """, (username, senha_hash, otp_secret))

        conn.commit()
        print("Usuário cadastrado com sucesso!")

        # Mostra para o usuario configurar
        print("\n=== CONFIGURAÇÃO 2FA ===")
        print("Adicione este código no Google Authenticator:")
        print(f"Chave secreta: {otp_secret}")

    except sqlite3.IntegrityError:
        print("Erro: usuário já existe!")

    finally:
        conn.close()


def login(username, password):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT password, otp_secret FROM usuarios
    WHERE username=?
    """, (username,))

    result = cursor.fetchone()
    conn.close()

    if result is None:
        print("Usuário não encontrado!")
        return False

    senha_hash, otp_secret = result

    # verificao de senha
    if not bcrypt.checkpw(password.encode(), senha_hash):
        print("Senha incorreta!")
        return False

    # Etapa 2FA
    totp = pyotp.TOTP(otp_secret)

    codigo = input("Digite o código 2FA: ")

    if totp.verify(codigo):
        print("Login completo (2FA OK)!")
        return True
    else:
        print("Código 2FA inválido!")
        return False


# MENU

def menu():
    while True:
        print("\n=== LOGIN BCRYPT + 2FA ===")
        print("1 - Registrar")
        print("2 - Login")
        print("3 - Sair")

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


if __name__ == "__main__":
    menu()