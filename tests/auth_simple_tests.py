import sys
import os
import sqlite3
import pyotp

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from db.database import criar_banco
from auth import auth_plain, auth_md5, auth_salt, auth_bcrypt, twoFA


def conectar():
    return sqlite3.connect("users.db")


def separar():
    print("\n" + "=" * 60)


def mostrar_resultado(descricao, esperado, obtido):
    print(descricao)
    print(f"Esperado: {esperado}")
    print(f"Obtido:   {obtido}")

    if esperado == obtido:
        print("Status: TESTE APROVADO")
    else:
        print("Status: TESTE REPROVADO")


def buscar_secret_2fa(usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT otp_secret
        FROM usuarios
        WHERE username=?
    """, (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return resultado[0]
    return None


def testar_cadastro(modulo, usuario, senha):
    print("\n[1] TESTE DE CADASTRO")
    print(f"Usuário de teste: {usuario}")
    modulo.registrar(usuario, senha)
    print("Resultado esperado: usuário cadastrado com sucesso.")


def testar_login_correto(modulo, usuario, senha):
    print("\n[2] TESTE DE LOGIN COM SENHA CORRETA")
    resultado = modulo.login(usuario, senha)
    mostrar_resultado(
        "Validação de autenticação com credenciais válidas",
        True,
        resultado
    )


def testar_login_incorreto(modulo, usuario, senha_errada):
    print("\n[3] TESTE DE LOGIN COM SENHA INCORRETA")
    resultado = modulo.login(usuario, senha_errada)
    mostrar_resultado(
        "Validação de rejeição de senha incorreta",
        False,
        resultado
    )


def testar_usuario_inexistente(modulo, usuario_inexistente, senha):
    print("\n[4] TESTE DE LOGIN COM USUÁRIO INEXISTENTE")
    resultado = modulo.login(usuario_inexistente, senha)
    mostrar_resultado(
        "Validação de rejeição para usuário não cadastrado",
        False,
        resultado
    )


def testar_metodo(nome_metodo, modulo, usuario, senha_correta, senha_errada):
    separar()
    print(f"TESTANDO MÉTODO: {nome_metodo}")

    testar_cadastro(modulo, usuario, senha_correta)
    testar_login_correto(modulo, usuario, senha_correta)
    testar_login_incorreto(modulo, usuario, senha_errada)
    testar_usuario_inexistente(modulo, usuario + "_nao_existe", senha_correta)


# ---------------- TESTES DO MÉTODO 2FA + BCRYPT ----------------

def testar_cadastro_2fa(modulo, usuario, senha):
    print("\n[1] TESTE DE CADASTRO")
    print(f"Usuário de teste: {usuario}")
    modulo.registrar(usuario, senha)
    print("Resultado esperado: usuário cadastrado com sucesso e chave 2FA criada.")


def testar_login_2fa_correto(modulo, usuario, senha):
    print("\n[2] TESTE DE LOGIN COM SENHA CORRETA + 2FA CORRETO")

    secret = buscar_secret_2fa(usuario)
    totp = pyotp.TOTP(secret)
    codigo = totp.now()

    resultado = modulo.login(usuario, senha, codigo)

    mostrar_resultado(
        "Validação de autenticação com senha e código 2FA válidos",
        True,
        resultado
    )


def testar_login_2fa_incorreto(modulo, usuario, senha):
    print("\n[3] TESTE DE LOGIN COM SENHA CORRETA + 2FA INCORRETO")

    codigo_errado = "000000"
    resultado = modulo.login(usuario, senha, codigo_errado)

    mostrar_resultado(
        "Validação de rejeição com código 2FA inválido",
        False,
        resultado
    )


def testar_login_2fa_senha_errada(modulo, usuario, senha_errada):
    print("\n[4] TESTE DE LOGIN COM SENHA INCORRETA + 2FA CORRETO")

    secret = buscar_secret_2fa(usuario)
    totp = pyotp.TOTP(secret)
    codigo = totp.now()

    resultado = modulo.login(usuario, senha_errada, codigo)

    mostrar_resultado(
        "Validação de rejeição com senha incorreta mesmo com 2FA válido",
        False,
        resultado
    )


def testar_usuario_2fa_inexistente(modulo, usuario_inexistente, senha):
    print("\n[5] TESTE DE LOGIN COM USUÁRIO INEXISTENTE")

    codigo = "123456"
    resultado = modulo.login(usuario_inexistente, senha, codigo)

    mostrar_resultado(
        "Validação de rejeição para usuário não cadastrado no método 2FA",
        False,
        resultado
    )


def testar_metodo_2fa(nome_metodo, modulo, usuario, senha_correta, senha_errada):
    separar()
    print(f"TESTANDO MÉTODO: {nome_metodo}")

    testar_cadastro_2fa(modulo, usuario, senha_correta)
    testar_login_2fa_correto(modulo, usuario, senha_correta)
    testar_login_2fa_incorreto(modulo, usuario, senha_correta)
    testar_login_2fa_senha_errada(modulo, usuario, senha_errada)
    testar_usuario_2fa_inexistente(modulo, usuario + "_nao_existe", senha_correta)


if __name__ == "__main__":
    criar_banco()

    testar_metodo(
        "a) Senha em Plain Text",
        auth_plain,
        "usuario_plain_teste",
        "Senha@123",
        "Errada@123"
    )

    testar_metodo(
        "b) Senha com Hash MD5",
        auth_md5,
        "usuario_md5_teste",
        "Senha@123",
        "Errada@123"
    )

    testar_metodo(
        "c) Senha com Hash + Salt",
        auth_salt,
        "usuario_salt_teste",
        "Senha@123",
        "Errada@123"
    )

    testar_metodo(
        "d) Senha com Bcrypt",
        auth_bcrypt,
        "usuario_bcrypt_teste",
        "Senha@123",
        "Errada@123"
    )

    testar_metodo_2fa(
        "e) 2FA + Bcrypt",
        twoFA,
        "usuario_2fa_teste",
        "Senha@123",
        "Errada@123"
    )