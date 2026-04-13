import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from auth import auth_bcrypt
from db.database import criar_banco


if __name__ == "__main__":
    criar_banco()

    usuario = "user_bruteforce"
    senha = "Senha@123"

    print("\n[1] Cadastro")
    auth_bcrypt.registrar(usuario, senha)

    tentativas = ["Senha@111", "Senha@222", "Senha@333", "Senha@123"]

    for tentativa in tentativas:
        print("\nTentando:", tentativa)
        auth_bcrypt.login(usuario, tentativa)