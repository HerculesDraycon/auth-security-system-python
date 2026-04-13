import re
from datetime import datetime, timedelta

#Funcao que verifica se a senha atende aos requisitos minimos de seguranca (Melhoria 2).
def validar_forca_senha(senha):
    if len(senha) < 8: return False, "A senha deve ter pelo menos 8 caracteres."
    if not re.search(r"[A-Z]", senha): return False, "A senha deve ter pelo menos uma letra maiúscula."
    if not re.search(r"[a-z]", senha): return False, "A senha deve ter pelo menos uma letra minúscula."
    if not re.search(r"[0-9]", senha): return False, "A senha deve ter pelo menos um número."
    if not re.search(r"[@#$%^&+=!*]", senha): return False, "A senha deve ter pelo menos um caractere especial (@#$%^&+=!*)."
    return True, "Senha forte."

#Funcao que analisa banco para ver se usuario ja sofreu bloqueio na rotina de seguranca (Melhoria 1).
def checar_bloqueio(cursor, username):
    cursor.execute("SELECT tentativas_falhas, bloqueado_ate FROM usuarios WHERE username=?", (username,))
    result = cursor.fetchone()
    if result is None:
        return False, False # false = não encontrado, login cuida disso
    
    tentativas, bloqueado_ate = result
    if bloqueado_ate:
        try:
            tempo_bloqueio = datetime.fromisoformat(bloqueado_ate)
            if datetime.now() < tempo_bloqueio:
                restante = (tempo_bloqueio - datetime.now()).seconds
                minutos = restante // 60
                segundos = restante % 60
                return True, f"Conta bloqueada. Tente novamente em {minutos}m {segundos}s."
            else:
                cursor.execute("UPDATE usuarios SET tentativas_falhas=0, bloqueado_ate=NULL WHERE username=?", (username,))
                return False, False
        except ValueError:
            pass
    return False, False

#Funcao para contar erros e realizar o bloqueio de rate limits caso bata 3 erros (Melhoria 1).
def registrar_tentativa_falha(cursor, conn, username):
    cursor.execute("SELECT tentativas_falhas FROM usuarios WHERE username=?", (username,))
    result = cursor.fetchone()
    if result:
        tentativas = result[0] + 1
        if tentativas >= 3:
            bloqueado_ate = (datetime.now() + timedelta(minutes=5)).isoformat()
            cursor.execute("UPDATE usuarios SET tentativas_falhas=?, bloqueado_ate=? WHERE username=?", (tentativas, bloqueado_ate, username))
            print("\nMúltiplas tentativas falhas. Conta bloqueada por 5 minutos.")
        else:
            cursor.execute("UPDATE usuarios SET tentativas_falhas=? WHERE username=?", (tentativas, username))
            print(f"\nSenha incorreta! Tentativas falhas: {tentativas}/3")
        conn.commit()

#Funcao para restaurar a conta para 0 erros parciais em caso de sucesso no login (Melhoria 1).
def resetar_tentativas(cursor, conn, username):
    cursor.execute("UPDATE usuarios SET tentativas_falhas=0, bloqueado_ate=NULL WHERE username=?", (username,))
    conn.commit()
