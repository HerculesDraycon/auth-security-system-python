import sys
import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from db.database import criar_banco
from auth import auth_bcrypt


def conectar():
    return sqlite3.connect("users.db")


def mostrar_estado_usuario(username):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, tentativas_falhas, bloqueado_ate
        FROM usuarios
        WHERE username=?
    """, (username,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

if __name__ == "__main__":
    criar_banco()

    usuario = "user_bloqueio"
    senha_correta = "Senha@123"
    senha_errada = "Erro@123"

    print("\n[1] Cadastro do usuário")
    auth_bcrypt.registrar(usuario, senha_correta)

    print("\n[2] Primeira tentativa incorreta")
    r1 = auth_bcrypt.login(usuario, senha_errada)
    print("Estado no banco:", mostrar_estado_usuario(usuario))

    print("\n[3] Segunda tentativa incorreta")
    r2 = auth_bcrypt.login(usuario, senha_errada)
    print("Estado no banco:", mostrar_estado_usuario(usuario))

    print("\n[4] Terceira tentativa incorreta")
    r3 = auth_bcrypt.login(usuario, senha_errada)
    print("Estado no banco:", mostrar_estado_usuario(usuario))

    print("\n[5] Tentativa com senha correta durante bloqueio")
    r4 = auth_bcrypt.login(usuario, senha_correta)
    print("Estado no banco:", mostrar_estado_usuario(usuario))