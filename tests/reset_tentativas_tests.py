import sys
import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from db.database import criar_banco
from auth import auth_bcrypt

def conectar():
    return sqlite3.connect("users.db")


def mostrar_tentativas(username):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tentativas_falhas FROM usuarios WHERE username=?
    """, (username,))

    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


if __name__ == "__main__":
    criar_banco()

    usuario = "user_reset"
    senha = "Senha@123"
    senha_errada = "Errada@123"

    print("\n[1] Cadastro")
    auth_bcrypt.registrar(usuario, senha)

    print("\n[2] Duas tentativas incorretas")
    auth_bcrypt.login(usuario, senha_errada)
    auth_bcrypt.login(usuario, senha_errada)

    print("Tentativas atuais:", mostrar_tentativas(usuario))

    print("\n[3] Login correto (deve resetar)")
    auth_bcrypt.login(usuario, senha)

    print("Tentativas após sucesso:", mostrar_tentativas(usuario))

    print("\n[4] Nova tentativa incorreta")
    auth_bcrypt.login(usuario, senha_errada)

    print("Tentativas agora:", mostrar_tentativas(usuario))