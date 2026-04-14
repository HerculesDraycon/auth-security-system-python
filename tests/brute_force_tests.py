import time
import hashlib
import bcrypt
import pyotp

# senha real
senha_real = "Senha@123"

# lista de tentativas
tentativas = [f"Senha@{i}" for i in range(200)] + ["Senha@123"]


# ---------------- MD5 ----------------
def brute_force_md5():
    hash_alvo = hashlib.md5(senha_real.encode()).hexdigest()

    start = time.time()

    for tentativa in tentativas:
        if hashlib.md5(tentativa.encode()).hexdigest() == hash_alvo:
            end = time.time()
            print("MD5 quebrado! Senha:", tentativa)
            print("Tempo:", end - start)
            return tentativa

    return None


# ---------------- BCRYPT ----------------
def brute_force_bcrypt():
    hash_alvo = bcrypt.hashpw(senha_real.encode(), bcrypt.gensalt())

    start = time.time()

    for tentativa in tentativas:
        if bcrypt.checkpw(tentativa.encode(), hash_alvo):
            end = time.time()
            print("Bcrypt quebrado! Senha:", tentativa)
            print("Tempo:", end - start)
            return tentativa

    return None


# ---------------- 2FA + BCRYPT ----------------
def brute_force_2fa_bcrypt():
    print("\n=== BRUTE FORCE 2FA + BCRYPT ===")

    # "Banco" simulado
    senha_hash = bcrypt.hashpw(senha_real.encode(), bcrypt.gensalt())

    # Configuração do 2FA
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)

    # ataque brute force
    start = time.time()
    senha_encontrada = None

    for tentativa in tentativas:
        if bcrypt.checkpw(tentativa.encode(), senha_hash):
            senha_encontrada = tentativa
            break

    end = time.time()

    if senha_encontrada:
        print("Senha descoberta:", senha_encontrada)
        print("Tempo para descobrir a senha:", end - start)

        # ---------------- tentativa SEM 2FA ----------------
        print("\n[TESTE] Tentativa de login sem código 2FA correto")

        codigo_errado = "000000"

        senha_ok = bcrypt.checkpw(senha_encontrada.encode(), senha_hash)
        codigo_ok = totp.verify(codigo_errado)

        if senha_ok and codigo_ok:
            print("FALHA: invasor conseguiu acesso")
        else:
            print("SUCESSO: 2FA bloqueou o invasor")

        # ---------------- tentativa COM 2FA ----------------
        print("\n[TESTE] Tentativa com senha + 2FA corretos")

        codigo_correto = totp.now()

        senha_ok = bcrypt.checkpw(senha_encontrada.encode(), senha_hash)
        codigo_ok = totp.verify(codigo_correto)

        if senha_ok and codigo_ok:
            print("SUCESSO: usuário legítimo autenticou")
        else:
            print("FALHA: usuário legítimo não conseguiu")

    else:
        print("Senha não encontrada.")


# ---------------- EXECUÇÃO ----------------
if __name__ == "__main__":
    print("\n=== BRUTE FORCE MD5 ===")
    brute_force_md5()

    print("\n=== BRUTE FORCE BCRYPT ===")
    brute_force_bcrypt()

    brute_force_2fa_bcrypt()