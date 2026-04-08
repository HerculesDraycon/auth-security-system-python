import hashlib

# Lista de senhas comuns

senhas_comuns = [
    "123456",
    "password",
    "admin",
    "qwerty"
]

hash_alvo = "e10adc3949ba59abbe56e057f20f883e"

for senha in senhas_comuns:

    if hashlib.md5(senha.encode()).hexdigest() == hash_alvo:

        print("Senha descoberta:", senha)

