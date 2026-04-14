SISTEMA DE AUTENTICAÇÃO SEGURO (PYTHON + SQLITE3)

Abril de 2026.

---

DESCRIÇÃO DO PROJETO

Este projeto tem como objetivo implementar e analisar diferentes métodos de autenticação de usuários, avaliando seus níveis de segurança e vulnerabilidades.

Foram desenvolvidas diferentes abordagens de armazenamento de senha, desde métodos inseguros até técnicas modernas utilizadas em sistemas reais.

---

OBJETIVO

* Implementar um sistema de autenticação em Python
* Comparar diferentes métodos de armazenamento de senha
* Avaliar vulnerabilidades e riscos de segurança
* Aplicar boas práticas de segurança da informação

---

FUNCIONALIDADES IMPLEMENTADAS

- Cadastro de usuários
- Login de usuários
- Diferentes métodos de autenticação
- Testes de vulnerabilidade
- Comparação de desempenho
- Autenticação em dois fatores (2FA)

---

MÉTODOS DE AUTENTICAÇÃO

1. Plain Text (Inseguro)

* Senhas armazenadas diretamente no banco
* Totalmente vulnerável

2. MD5

* Senhas armazenadas como hash
* Vulnerável a ataques de força bruta e rainbow tables

3. SHA-256 com Salt

* Adiciona valor aleatório à senha
* Aumenta a segurança
* Ainda vulnerável a brute force lento

4. Bcrypt (Recomendado)

* Salt automático
* Alto custo computacional
* Proteção contra ataques modernos

---

AUTENTICAÇÃO EM DOIS FATORES (2FA)

Foi implementado 2FA utilizando a biblioteca pyotp.

Fluxo:

1. Usuário realiza login com senha
2. Sistema solicita código gerado por aplicativo autenticador
3. Acesso liberado apenas com código válido

Isso adiciona uma camada extra de segurança ao sistema.

---

BANCO DE DADOS

Tabela: usuarios

Campos:

* id
* username
* password
* salt
* otp_secret

---

VULNERABILIDADES IDENTIFICADAS

* Plain text expõe diretamente a senha
* MD5 pode ser quebrado facilmente
* SHA-256 ainda é rápido para ataques

---

MELHORIAS IMPLEMENTADAS

- Uso de bcrypt
- Uso de salt
- Autenticação em dois fatores (2FA)
- Organização modular do projeto

---

COMO EXECUTAR

1. Instalar dependências:

pip install bcrypt pyotp

2. Criar o banco:

python db/database.py

3. (Caso necessário) adicionar coluna 2FA:

ALTER TABLE usuarios ADD COLUMN otp_secret TEXT;

4. Executar sistema:

python main.py

---

COMO USAR O 2FA

1. Registrar usuário
2. Copiar a chave secreta exibida
3. Adicionar no Google Authenticator
4. Informar o código gerado no login

---

CONCLUSÃO

O projeto demonstra que métodos simples de armazenamento de senha são altamente vulneráveis. A utilização de bcrypt, combinada com autenticação em dois fatores, fornece um nível de segurança adequado para aplicações reais.
