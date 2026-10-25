# Gerador de senhas fortes
# Feito só com Python, sem instalar nada.
#
# O programa NÃO pergunta nada sobre a pessoa. Ele cria senhas aleatórias
# e garante que a mesma senha nunca seja entregue duas vezes.

import hashlib
import os
import random
import secrets
import string

maiusculas = string.ascii_uppercase
minusculas = string.ascii_lowercase
numeros = string.digits
especiais = "@#$!?*%&-_+="

TAMANHO_MINIMO = 8
TAMANHO_MAXIMO = 64
TAMANHO_PADRAO = 12

pasta = os.path.dirname(os.path.abspath(__file__))

# Arquivo INTERNO: guarda só os "códigos" (hash) das senhas que já foram
# geradas, para nunca repetir. As senhas NÃO ficam nele.
ARQUIVO_REGISTRO = os.path.join(pasta, "registro_codigos.txt")

# nome que esse arquivo tinha antes (usado só para não perder o histórico)
ARQUIVO_ANTIGO = os.path.join(pasta, "senhas_geradas.txt")

# Arquivo OPCIONAL: só é criado se a pessoa pedir para salvar a senha.
# Esse sim guarda a senha de verdade, para a pessoa poder consultar.
ARQUIVO_SENHAS = os.path.join(pasta, "minhas_senhas.txt")


# ---------------------------------------------------------------------------
# Gerando a senha
# ---------------------------------------------------------------------------

def gerar_senha(tamanho):
    if tamanho < TAMANHO_MINIMO:
        tamanho = TAMANHO_MINIMO

    # começa com 1 de cada tipo, assim a senha sempre cumpre as regras
    # (usamos "secrets" em vez de "random" porque ele é feito para segurança)
    senha = [
        secrets.choice(maiusculas),
        secrets.choice(minusculas),
        secrets.choice(numeros),
        secrets.choice(especiais),
    ]

    # o resto é sorteado entre todos os caracteres
    todos = maiusculas + minusculas + numeros + especiais
    while len(senha) < tamanho:
        senha.append(secrets.choice(todos))

    # embaralha, senão as 4 primeiras posições seriam sempre
    # maiúscula, minúscula, número e símbolo
    random.SystemRandom().shuffle(senha)

    return "".join(senha)


def tem_padrao_facil(senha):
    # procura 3 caracteres seguidos iguais (aaa) ou em sequência (abc, 321)
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
# Registro: evita que duas pessoas recebam a mesma senha
# ---------------------------------------------------------------------------

def criar_codigo(senha):
    # transforma a senha num "código" (hash SHA-256).
    # Não dá para descobrir a senha a partir do código, então o arquivo
    # pode guardar os códigos sem expor nenhuma senha.
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def migrar_registro_antigo(antigo=ARQUIVO_ANTIGO, novo=ARQUIVO_REGISTRO):
    # se existir o arquivo com o nome antigo, passa ele para o nome novo
    # (assim as senhas que já foram geradas continuam sendo lembradas)
    if os.path.exists(antigo) and not os.path.exists(novo):
        os.rename(antigo, novo)


def ler_registro(arquivo=ARQUIVO_REGISTRO):
    if not os.path.exists(arquivo):
        return []

    codigos = []
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            # ignora linhas vazias e os comentários (que começam com #)
            if linha != "" and not linha.startswith("#"):
                codigos.append(linha)
    return codigos


def salvar_no_registro(codigo, arquivo=ARQUIVO_REGISTRO):
    arquivo_novo = not os.path.exists(arquivo)
    with open(arquivo, "a", encoding="utf-8") as f:
        if arquivo_novo:
            f.write("# Arquivo interno do programa. Guarda so os codigos (hash)\n")
            f.write("# das senhas ja geradas. As senhas NAO ficam aqui.\n")
            f.write("# Nao apague, senao o programa esquece o que ja gerou.\n")
        f.write(codigo + "\n")


def gerar_senha_unica(tamanho, arquivo=ARQUIVO_REGISTRO):
    usadas = ler_registro(arquivo)

    while True:
        senha = gerar_senha(tamanho)

        # senha com padrão fácil: descarta e sorteia outra
        if tem_padrao_facil(senha):
            continue

        # senha que já foi entregue antes: descarta e sorteia outra
        codigo = criar_codigo(senha)
        if codigo in usadas:
            continue

        # passou nos dois testes: registra e entrega
        salvar_no_registro(codigo, arquivo)
        return senha


# ---------------------------------------------------------------------------
# Salvando a senha para a pessoa (opcional)
# ---------------------------------------------------------------------------

def salvar_senha_em_arquivo(senha, nome, arquivo=ARQUIVO_SENHAS):
    with open(arquivo, "a", encoding="utf-8") as f:
        f.write(nome + ": " + senha + "\n")


# ---------------------------------------------------------------------------
# Nível da senha gerada
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

    # senhas maiores ganham pontos extras
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
# Parte do terminal
# ---------------------------------------------------------------------------

def pedir_tamanho():
    while True:
        texto = input(f"Tamanho da senha ({TAMANHO_MINIMO} a {TAMANHO_MAXIMO}): ")
        if texto.isdigit():
            tamanho = int(texto)
            if tamanho >= TAMANHO_MINIMO and tamanho <= TAMANHO_MAXIMO:
                return tamanho
        print(f"Digite um número entre {TAMANHO_MINIMO} e {TAMANHO_MAXIMO}.")


def mostrar_senha(senha):
    print()
    print("=" * 40)
    print("  SUA SENHA:")
    print()
    print("    " + senha)
    print()
    print("  Nível:", calcular_nivel(senha))
    print("=" * 40)


def oferecer_salvar(senha):
    print()
    resposta = input("Quer salvar essa senha em um arquivo de texto? (s/n): ")
    if resposta.strip().lower() != "s":
        print("Ok, não salvei. Anote a senha agora, ela não fica guardada.")
        return

    nome = input("Para que é essa senha? (ex: Instagram): ").strip()
    if nome == "":
        nome = "sem nome"

    salvar_senha_em_arquivo(senha, nome)
    print()
    print("Senha salva em:")
    print(ARQUIVO_SENHAS)
    print("Atenção: quem abrir esse arquivo consegue ver a senha.")


def main():
    migrar_registro_antigo()

    print("=" * 40)
    print("      GERADOR DE SENHAS FORTES")
    print("=" * 40)

    tamanho = TAMANHO_PADRAO

    while True:
        print()
        print("Tamanho atual:", tamanho)
        print("1 - Gerar uma senha")
        print("2 - Mudar o tamanho")
        print("3 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            senha = gerar_senha_unica(tamanho)
            mostrar_senha(senha)
            oferecer_salvar(senha)
            print()
            input("Aperte Enter para voltar ao menu...")
        elif opcao == "2":
            tamanho = pedir_tamanho()
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")

    print("Até mais!")


if __name__ == "__main__":
    main()
