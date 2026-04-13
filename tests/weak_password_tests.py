import sys
import os
import random

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from db.database import criar_banco
from auth import auth_plain

senhas_fracas = ["123", "123456", "admin", "password"]

if __name__ == "__main__":
    criar_banco()

    for senha in senhas_fracas:
        usuario = f"user_{random.randint(1000,9999)}"
        print(f"\nTestando senha fraca: {senha}")
        auth_plain.registrar(usuario, senha)