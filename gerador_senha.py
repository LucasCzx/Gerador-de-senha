# Gerador de senhas fortes
# Feito só com Python, não precisa instalar nada.
#
# Como o programa pensa:
#   1. Ele não pergunta nada sobre você.
#   2. Ele não guarda as senhas em lugar nenhum. A senha aparece na tela
#      e, quando você aperta Enter, a tela é limpa.
#   3. Pra não entregar a mesma senha duas vezes, ele guarda só um
#      "código" de cada senha (um hash). Com o código não dá pra
#      descobrir qual era a senha.

import hashlib
import os
import random
import secrets
import string

maiusculas = string.ascii_uppercase
minusculas = string.ascii_lowercase
numeros = string.digits
especiais = "@#$!?*%&-_+="

TAMANHO_MINIMO = 12
TAMANHO_MAXIMO = 64
TAMANHO_PADRAO = 16

# Quantas vezes o programa repete a conta que cria o código da senha.
# É lento de propósito: pra você são uns 0,04 segundo, mas pra quem tentasse
# adivinhar senhas a partir dos códigos, fica muito mais trabalhoso.
ITERACOES = 200000

# O registro fica na pasta pessoal de cada pessoa (ex.: C:\Users\Nome\.gerador_senha)
# e não na pasta do programa. Assim ele nunca vai parar no GitHub por engano.
pasta_do_usuario = os.path.join(os.path.expanduser("~"), ".gerador_senha")
ARQUIVO_REGISTRO = os.path.join(pasta_do_usuario, "registro_codigos.txt")

CABECALHO = (
    "# Arquivo interno do gerador de senhas. Nao apague e nao compartilhe.\n"
    "# Aqui ficam so os codigos (hash) das senhas ja geradas, nunca as senhas.\n"
)


# ---------------------------------------------------------------------------
# Criando a senha
# ---------------------------------------------------------------------------

def gerar_senha(tamanho):
    if tamanho < TAMANHO_MINIMO:
        tamanho = TAMANHO_MINIMO

    # Começa com um caractere de cada tipo, assim a senha sempre tem
    # maiúscula, minúscula, número e símbolo.
    # (Usamos "secrets" e não "random" porque o secrets foi feito para segurança.)
    senha = [
        secrets.choice(maiusculas),
        secrets.choice(minusculas),
        secrets.choice(numeros),
        secrets.choice(especiais),
    ]

    # O resto das posições é sorteado entre todos os caracteres
    todos = maiusculas + minusculas + numeros + especiais
    while len(senha) < tamanho:
        senha.append(secrets.choice(todos))

    # Embaralha tudo. Se não embaralhasse, os 4 primeiros caracteres seriam
    # sempre maiúscula, minúscula, número e símbolo, nessa ordem.
    random.SystemRandom().shuffle(senha)

    return "".join(senha)


def tem_padrao_facil(senha):
    # Procura 3 caracteres seguidos iguais (aaa) ou em sequência (abc, 321)
    for i in range(len(senha) - 2):
        a = senha[i]
        b = senha[i + 1]
        c = senha[i + 2]

        if a == b and b == c:
            return True
        if ord(b) == ord(a) + 1 and ord(c) == ord(b) + 1:
            return True
        if ord(b) == ord(a) - 1 and ord(c) == ord(b) - 1:
            return True
    return False


# ---------------------------------------------------------------------------
# Registro: pra nunca entregar a mesma senha duas vezes
# ---------------------------------------------------------------------------

def criar_codigo(senha, salt):
    # Transforma a senha num código (hash PBKDF2-SHA256).
    # O "salt" é um texto aleatório que cada instalação sorteia uma vez.
    # Ele faz o código da sua senha ser diferente do código da mesma senha
    # em outro computador.
    codigo = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        bytes.fromhex(salt),
        ITERACOES,
    )
    return codigo.hex()


def abrir_registro_para_escrever(arquivo):
    # Cria a pasta do registro se ela ainda não existir (só o dono acessa)
    pasta = os.path.dirname(arquivo)
    if pasta != "":
        os.makedirs(pasta, mode=0o700, exist_ok=True)

    arquivo_novo = not os.path.exists(arquivo)

    # O 0o600 quer dizer: só o dono do arquivo pode ler e escrever.
    # (Vale no Linux e no Mac. No Windows, quem protege é a sua conta de usuário.)
    descritor = os.open(arquivo, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    f = os.fdopen(descritor, "a", encoding="utf-8")

    if arquivo_novo:
        f.write(CABECALHO)
    return f


def ler_linhas_do_registro(arquivo):
    # Devolve só as linhas que importam (pula as vazias e os comentários com #)
    if not os.path.exists(arquivo):
        return []

    linhas = []
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha != "" and not linha.startswith("#"):
                linhas.append(linha)
    return linhas


def ler_salt(arquivo=ARQUIVO_REGISTRO):
    for linha in ler_linhas_do_registro(arquivo):
        if linha.startswith("salt="):
            return linha[5:]
    return None


def garantir_salt(arquivo=ARQUIVO_REGISTRO):
    # Na primeira vez que o programa roda, sorteia o salt e guarda no registro.
    # Nas próximas vezes, só usa o que já está lá.
    salt = ler_salt(arquivo)
    if salt is None:
        salt = secrets.token_hex(16)
        with abrir_registro_para_escrever(arquivo) as f:
            f.write("salt=" + salt + "\n")
    return salt


def ler_registro(arquivo=ARQUIVO_REGISTRO):
    # Devolve só os códigos das senhas (sem a linha do salt)
    codigos = []
    for linha in ler_linhas_do_registro(arquivo):
        if not linha.startswith("salt="):
            codigos.append(linha)
    return codigos


def salvar_no_registro(codigo, arquivo=ARQUIVO_REGISTRO):
    with abrir_registro_para_escrever(arquivo) as f:
        f.write(codigo + "\n")


def gerar_senha_unica(tamanho, arquivo=ARQUIVO_REGISTRO):
    salt = garantir_salt(arquivo)
    usadas = set(ler_registro(arquivo))

    while True:
        senha = gerar_senha(tamanho)

        # Senha com padrão fácil? Joga fora e sorteia outra.
        if tem_padrao_facil(senha):
            continue

        # Senha que já foi entregue antes? Joga fora e sorteia outra.
        codigo = criar_codigo(senha, salt)
        if codigo in usadas:
            continue

        # Passou nos dois testes: guarda o código (só o código) e entrega.
        salvar_no_registro(codigo, arquivo)
        return senha


# ---------------------------------------------------------------------------
# Nível da senha
# ---------------------------------------------------------------------------

def tem_maiuscula(senha):
    for letra in senha:
        if letra.isupper():
            return True
    return False


def tem_minuscula(senha):
    for letra in senha:
        if letra.islower():
            return True
    return False


def tem_numero(senha):
    for letra in senha:
        if letra.isdigit():
            return True
    return False


def tem_especial(senha):
    for letra in senha:
        if letra in especiais:
            return True
    return False


def calcular_nivel(senha):
    # 1 ponto para cada regra básica
    pontos = 0
    if len(senha) >= 8:
        pontos = pontos + 1
    if tem_maiuscula(senha) and tem_minuscula(senha):
        pontos = pontos + 1
    if tem_numero(senha):
        pontos = pontos + 1
    if tem_especial(senha):
        pontos = pontos + 1

    # Senhas maiores ganham pontos extras
    if len(senha) >= 12:
        pontos = pontos + 1
    if len(senha) >= 16:
        pontos = pontos + 1

    if pontos <= 2:
        return "Fraca"
    elif pontos <= 4:
        return "Média"
    elif pontos == 5:
        return "Forte"
    else:
        return "Muito forte"


# ---------------------------------------------------------------------------
# Conversa com a pessoa (terminal)
# ---------------------------------------------------------------------------

def limpar_tela():
    # Apaga o que está na tela pra senha não ficar à vista de ninguém.
    # Alguns terminais ainda guardam o histórico mais acima, então se quiser
    # ter certeza, feche a janela do terminal depois de guardar a senha.
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def pedir_tamanho():
    while True:
        texto = input(f"Quantos caracteres você quer? ({TAMANHO_MINIMO} a {TAMANHO_MAXIMO}): ")
        if texto.isdigit():
            tamanho = int(texto)
            if tamanho >= TAMANHO_MINIMO and tamanho <= TAMANHO_MAXIMO:
                return tamanho
        print(f"Ops, digite um número entre {TAMANHO_MINIMO} e {TAMANHO_MAXIMO}.")


def mostrar_senha(senha):
    print()
    print("=" * 40)
    print("  PRONTO! SUA SENHA NOVA:")
    print()
    print("    " + senha)
    print()
    print("  Nível:", calcular_nivel(senha))
    print("=" * 40)
    print()
    print("Eu não guardo essa senha em lugar nenhum.")
    print("Copie agora e guarde num gerenciador de senhas.")


def main():
    print("=" * 40)
    print("      GERADOR DE SENHAS FORTES")
    print("=" * 40)
    print("Aqui as senhas são criadas na hora e não ficam guardadas.")

    tamanho = TAMANHO_PADRAO

    while True:
        print()
        print("Tamanho atual:", tamanho, "caracteres")
        print("1 - Gerar uma senha")
        print("2 - Mudar o tamanho")
        print("3 - Sair")
        opcao = input("O que você quer fazer? ")

        if opcao == "1":
            senha = gerar_senha_unica(tamanho)
            mostrar_senha(senha)
            print()
            input("Quando já tiver guardado a senha, aperte Enter pra limpar a tela...")
            limpar_tela()
        elif opcao == "2":
            tamanho = pedir_tamanho()
        elif opcao == "3":
            break
        else:
            print("Não entendi, escolha 1, 2 ou 3.")

    print("Até a próxima!")


if __name__ == "__main__":
    main()
