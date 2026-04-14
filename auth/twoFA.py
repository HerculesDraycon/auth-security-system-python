import sqlite3
import bcrypt
import pyotp
from datetime import datetime, timedelta

LIMITE_TENTATIVAS = 3
TEMPO_BLOQUEIO_MINUTOS = 1


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
        INSERT INTO usuarios (username, password, otp_secret, tentativas_falhas, bloqueado_ate)
        VALUES (?, ?, ?, 0, NULL)
        """, (username, senha_hash, otp_secret))

        conn.commit()
        print("Usuário cadastrado com sucesso!")

        print("\n=== CONFIGURAÇÃO 2FA ===")
        print("Adicione este código no Google Authenticator:")
        print(f"Chave secreta: {otp_secret}")

    except sqlite3.IntegrityError:
        print("Erro: usuário já existe!")

    finally:
        conn.close()


def login(username, password, codigo=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT password, otp_secret, tentativas_falhas, bloqueado_ate
    FROM usuarios
    WHERE username=?
    """, (username,))

    result = cursor.fetchone()

    if result is None:
        conn.close()
        print("Usuário não encontrado!")
        return False

    senha_hash, otp_secret, tentativas_falhas, bloqueado_ate = result

    # Verifica se está bloqueado
    if bloqueado_ate is not None:
        horario_bloqueio = datetime.fromisoformat(bloqueado_ate)
        if datetime.now() < horario_bloqueio:
            conn.close()
            print(f"Usuário bloqueado até {bloqueado_ate}")
            return False
        else:
            # desbloqueia automaticamente se o tempo passou
            cursor.execute("""
            UPDATE usuarios
            SET tentativas_falhas = 0, bloqueado_ate = NULL
            WHERE username=?
            """, (username,))
            conn.commit()
            tentativas_falhas = 0
            bloqueado_ate = None

    # Verifica senha
    if not bcrypt.checkpw(password.encode(), senha_hash):
        tentativas_falhas += 1

        if tentativas_falhas >= LIMITE_TENTATIVAS:
            bloqueado_ate = (datetime.now() + timedelta(minutes=TEMPO_BLOQUEIO_MINUTOS)).isoformat()
            cursor.execute("""
            UPDATE usuarios
            SET tentativas_falhas=?, bloqueado_ate=?
            WHERE username=?
            """, (tentativas_falhas, bloqueado_ate, username))
            conn.commit()
            conn.close()
            print(f"Senha incorreta! Usuário bloqueado até {bloqueado_ate}")
            return False
        else:
            cursor.execute("""
            UPDATE usuarios
            SET tentativas_falhas=?
            WHERE username=?
            """, (tentativas_falhas, username))
            conn.commit()
            conn.close()
            print(f"Senha incorreta! Tentativa {tentativas_falhas} de {LIMITE_TENTATIVAS}.")
            return False

    # Etapa 2FA
    totp = pyotp.TOTP(otp_secret)

    if codigo is None:
        codigo = input("Digite o código 2FA: ")

    if not totp.verify(codigo):
        tentativas_falhas += 1

        if tentativas_falhas >= LIMITE_TENTATIVAS:
            bloqueado_ate = (datetime.now() + timedelta(minutes=TEMPO_BLOQUEIO_MINUTOS)).isoformat()
            cursor.execute("""
            UPDATE usuarios
            SET tentativas_falhas=?, bloqueado_ate=?
            WHERE username=?
            """, (tentativas_falhas, bloqueado_ate, username))
            conn.commit()
            conn.close()
            print(f"Código 2FA inválido! Usuário bloqueado até {bloqueado_ate}")
            return False
        else:
            cursor.execute("""
            UPDATE usuarios
            SET tentativas_falhas=?
            WHERE username=?
            """, (tentativas_falhas, username))
            conn.commit()
            conn.close()
            print(f"Código 2FA inválido! Tentativa {tentativas_falhas} de {LIMITE_TENTATIVAS}.")
            return False

    # Se tudo estiver certo, zera tentativas
    cursor.execute("""
    UPDATE usuarios
    SET tentativas_falhas = 0, bloqueado_ate = NULL
    WHERE username=?
    """, (username,))
    conn.commit()
    conn.close()

    print("Login completo (2FA OK)!")
    return True


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