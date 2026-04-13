import sys
import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from db.database import criar_banco
from auth import auth_bcrypt
from auth import auth_md5
from auth import auth_salt

def conectar():
    return sqlite3.connect("users.db")


def buscar_password(username):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE username=?", (username,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


def separar():
    print("\n" + "=" * 50)


if __name__ == "__main__":
    criar_banco()

    senha = "Senha@123"

    auth_md5.registrar("md5_user1", senha)
    auth_md5.registrar("md5_user2", senha)

    auth_salt.registrar("salt_user1", senha)
    auth_salt.registrar("salt_user2", senha)

    auth_bcrypt.registrar("bcrypt_user1", senha)
    auth_bcrypt.registrar("bcrypt_user2", senha)

    separar()
    print("MD5")
    print(buscar_password("md5_user1"))
    print(buscar_password("md5_user2"))

    separar()
    print("SHA256 + SALT")
    print(buscar_password("salt_user1"))
    print(buscar_password("salt_user2"))

    separar()
    print("BCRYPT")
    print(buscar_password("bcrypt_user1"))
    print(buscar_password("bcrypt_user2"))