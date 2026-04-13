import time
import hashlib
import bcrypt

# senha real (agora forte)
senha_real = "Senha@123"

# lista de tentativa (incluindo a correta no final)
tentativas = [f"Senha@{i}" for i in range(200)] + ["Senha@123"]


def brute_force_md5():
    hash_alvo = hashlib.md5(senha_real.encode()).hexdigest()

    start = time.time()

    for tentativa in tentativas:
        if hashlib.md5(tentativa.encode()).hexdigest() == hash_alvo:
            end = time.time()
            print("MD5 quebrado! Senha:", tentativa)
            print("Tempo:", end - start)
            return


def brute_force_bcrypt():
    hash_alvo = bcrypt.hashpw(senha_real.encode(), bcrypt.gensalt())

    start = time.time()

    for tentativa in tentativas:
        if bcrypt.checkpw(tentativa.encode(), hash_alvo):
            end = time.time()
            print("Bcrypt quebrado! Senha:", tentativa)
            print("Tempo:", end - start)
            return


if __name__ == "__main__":
    print("\n=== BRUTE FORCE MD5 ===")
    brute_force_md5()

    print("\n=== BRUTE FORCE BCRYPT ===")
    brute_force_bcrypt()