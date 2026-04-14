from auth.auth_plain import menu as menu_plain
from auth.auth_md5 import menu as menu_md5
from auth.auth_salt import menu as menu_salt
from auth.auth_bcrypt import menu as menu_bcrypt
from auth.twoFA import menu as t_fa

def main():
    while True:
        print("\n=== Sistema de Autenticação ===")
        print("1 - Plain Text")
        print("2 - MD5")
        print("3 - Salt")
        print("4 - BCRYPT")
        print("5 - 2FA + BCRYPT")
        print("6 - Sair")

        op = input("Escolha: ")

        if op == "1":
            menu_plain()

        elif op == "2":
            menu_md5()

        elif op == "3":
            menu_salt()

        elif op == "4":
            menu_bcrypt()

        elif op == "5":
            t_fa()

        elif op == "6":
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()