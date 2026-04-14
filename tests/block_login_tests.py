import sys
import os
import sqlite3
import pyotp

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from db.database import criar_banco
from auth import twoFA


def conectar():
    return sqlite3.connect("users.db")


def mostrar_estado_usuario(username):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, tentativas_falhas, bloqueado_ate, otp_secret
        FROM usuarios
        WHERE username=?
    """, (username,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado


def buscar_secret_2fa(usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT otp_secret FROM usuarios WHERE username = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return resultado[0]
    return None


if __name__ == "__main__":
    criar_banco()

    usuario = "user_bloqueio_2fa"
    senha_correta = "Senha@123"
    senha_errada = "Erro@123"

    print("\n[1] Cadastro do usuário com 2FA + Bcrypt")
    twoFA.registrar(usuario, senha_correta)

    secret = buscar_secret_2fa(usuario)
    totp = pyotp.TOTP(secret)

    print("Estado no banco após cadastro:", mostrar_estado_usuario(usuario))

    print("\n[2] Primeira tentativa incorreta (senha correta + código 2FA errado)")
    r1 = twoFA.login(usuario, senha_correta, "000000")
    print("Resultado login:", r1)
    print("Estado no banco:", mostrar_estado_usuario(usuario))

    print("\n[3] Segunda tentativa incorreta (senha correta + código 2FA errado)")
    r2 = twoFA.login(usuario, senha_correta, "000000")
    print("Resultado login:", r2)
    print("Estado no banco:", mostrar_estado_usuario(usuario))

    print("\n[4] Terceira tentativa incorreta (senha correta + código 2FA errado)")
    r3 = twoFA.login(usuario, senha_correta, "000000")
    print("Resultado login:", r3)
    print("Estado no banco:", mostrar_estado_usuario(usuario))

    print("\n[5] Tentativa com senha correta e 2FA correto durante bloqueio")
    codigo_correto = totp.now()
    r4 = twoFA.login(usuario, senha_correta, codigo_correto)
    print("Resultado login:", r4)
    print("Estado no banco:", mostrar_estado_usuario(usuario))