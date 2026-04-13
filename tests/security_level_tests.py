import sys
import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from db.database import criar_banco
from auth import auth_bcrypt
from auth import auth_plain
from auth import auth_md5
from auth import auth_salt

def conectar():
    return sqlite3.connect("users.db")


def mostrar_dados_usuario(username):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, password, salt FROM usuarios WHERE username=?
    """, (username,))

    resultado = cursor.fetchone()
    conn.close()
    return resultado


def separar():
    print("\n" + "=" * 50)


if __name__ == "__main__":
    criar_banco()

    senha = "Senha@123"

    auth_plain.registrar("seg_plain", senha)
    auth_md5.registrar("seg_md5", senha)
    auth_salt.registrar("seg_salt", senha)
    auth_bcrypt.registrar("seg_bcrypt", senha)

    separar()
    print("DADOS SALVOS NO BANCO:")

    for user in ["seg_plain", "seg_md5", "seg_salt", "seg_bcrypt"]:
        print(f"\nUsuário: {user}")
        print(mostrar_dados_usuario(user))