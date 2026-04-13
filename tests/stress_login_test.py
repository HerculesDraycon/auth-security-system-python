import sys
import os
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from db.database import criar_banco
from auth import auth_bcrypt


if __name__ == "__main__":
    criar_banco()

    usuario = "user_stress"
    senha = "Senha@123"
    senha_errada = "Errada@123"

    print("\n[1] Cadastro")
    auth_bcrypt.registrar(usuario, senha)

    print("\n[2] Iniciando teste de exaustão")

    inicio = time.time()

    for i in range(50):
        print(f"\nTentativa {i+1}")
        auth_bcrypt.login(usuario, senha_errada)

    fim = time.time()

    print("\nTempo total:", fim - inicio)