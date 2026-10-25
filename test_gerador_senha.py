# Testes simples do gerador de senhas
# Para rodar: python test_gerador_senha.py

import os

import gerador_senha as g

arquivo_teste = "registro_teste.txt"
arquivo_senhas_teste = "senhas_teste.txt"


def apagar_arquivo(nome):
    if os.path.exists(nome):
        os.remove(nome)


def teste_tamanho_correto():
    for tamanho in [8, 12, 20, 64]:
        assert len(g.gerar_senha(tamanho)) == tamanho


def teste_tamanho_minimo():
    # se pedirem menos que 8, o programa entrega 8
    assert len(g.gerar_senha(3)) == 8


def teste_tem_todos_os_tipos():
    for i in range(300):
        senha = g.gerar_senha(12)
        assert g.tem_maiuscula(senha)
        assert g.tem_minuscula(senha)
        assert g.tem_numero(senha)
        assert g.tem_especial(senha)


def teste_padroes_faceis():
    assert g.tem_padrao_facil("xaaay") == True    # repetição
    assert g.tem_padrao_facil("x1234y") == True   # sequência crescente
    assert g.tem_padrao_facil("xcbay") == True    # sequência decrescente
    assert g.tem_padrao_facil("Aq7#mK!x2Zp9") == False


def teste_senhas_nunca_repetem():
    apagar_arquivo(arquivo_teste)
    senhas = []
    for i in range(300):
        senhas.append(g.gerar_senha_unica(12, arquivo_teste))

    assert len(set(senhas)) == 300                    # nenhuma repetida
    assert len(g.ler_registro(arquivo_teste)) == 300  # todas registradas
    apagar_arquivo(arquivo_teste)


def teste_senhas_unicas_sem_padrao_facil():
    apagar_arquivo(arquivo_teste)
    for i in range(100):
        senha = g.gerar_senha_unica(12, arquivo_teste)
        assert g.tem_padrao_facil(senha) == False
    apagar_arquivo(arquivo_teste)


def teste_conflito_e_evitado():
    # aqui a gente "força" o gerador a sortear a mesma senha duas vezes
    # pra ver se ele percebe o conflito e tenta de novo
    apagar_arquivo(arquivo_teste)
    sequencia = ["Aq7#mK!x2Zp9", "Aq7#mK!x2Zp9", "Bw4$nR&y8Lc3"]
    posicao = [0]

    def sorteio_falso(tamanho):
        senha = sequencia[posicao[0]]
        posicao[0] = posicao[0] + 1
        return senha

    original = g.gerar_senha
    g.gerar_senha = sorteio_falso
    try:
        primeira = g.gerar_senha_unica(12, arquivo_teste)
        segunda = g.gerar_senha_unica(12, arquivo_teste)
    finally:
        g.gerar_senha = original  # devolve a função verdadeira
        apagar_arquivo(arquivo_teste)

    assert primeira == "Aq7#mK!x2Zp9"
    assert segunda == "Bw4$nR&y8Lc3"   # a repetida foi descartada


def teste_registro_nao_guarda_a_senha():
    apagar_arquivo(arquivo_teste)
    senha = g.gerar_senha_unica(12, arquivo_teste)

    with open(arquivo_teste, "r", encoding="utf-8") as f:
        conteudo = f.read()
    apagar_arquivo(arquivo_teste)

    assert senha not in conteudo                  # a senha não aparece
    assert g.criar_codigo(senha) in conteudo      # só o código dela


def teste_registro_ignora_comentarios():
    # o arquivo começa com linhas de aviso (#), que não podem virar "código"
    apagar_arquivo(arquivo_teste)
    g.salvar_no_registro("abc123", arquivo_teste)
    g.salvar_no_registro("def456", arquivo_teste)

    with open(arquivo_teste, "r", encoding="utf-8") as f:
        primeira_linha = f.readline()
    codigos = g.ler_registro(arquivo_teste)
    apagar_arquivo(arquivo_teste)

    assert primeira_linha.startswith("#")
    assert codigos == ["abc123", "def456"]


def teste_salvar_senha_em_arquivo():
    apagar_arquivo(arquivo_senhas_teste)
    g.salvar_senha_em_arquivo("Aq7#mK!x2Zp9", "Instagram", arquivo_senhas_teste)
    g.salvar_senha_em_arquivo("Bw4$nR&y8Lc3", "Email", arquivo_senhas_teste)

    with open(arquivo_senhas_teste, "r", encoding="utf-8") as f:
        linhas = f.read().split("\n")
    apagar_arquivo(arquivo_senhas_teste)

    assert linhas[0] == "Instagram: Aq7#mK!x2Zp9"
    assert linhas[1] == "Email: Bw4$nR&y8Lc3"


def teste_migrar_registro_antigo():
    antigo = "registro_antigo_teste.txt"
    novo = "registro_novo_teste.txt"
    apagar_arquivo(antigo)
    apagar_arquivo(novo)

    with open(antigo, "w", encoding="utf-8") as f:
        f.write("codigo1\ncodigo2\n")

    g.migrar_registro_antigo(antigo, novo)

    existe_antigo = os.path.exists(antigo)
    codigos = g.ler_registro(novo)
    apagar_arquivo(antigo)
    apagar_arquivo(novo)

    assert existe_antigo == False
    assert codigos == ["codigo1", "codigo2"]


todos = [teste_tamanho_correto, teste_tamanho_minimo,
         teste_tem_todos_os_tipos, teste_padroes_faceis,
         teste_senhas_nunca_repetem, teste_senhas_unicas_sem_padrao_facil,
         teste_conflito_e_evitado, teste_registro_nao_guarda_a_senha,
         teste_registro_ignora_comentarios, teste_salvar_senha_em_arquivo,
         teste_migrar_registro_antigo]

falhas = 0
for teste in todos:
    try:
        teste()
        print("OK   ", teste.__name__)
    except AssertionError:
        print("ERRO ", teste.__name__)
        falhas = falhas + 1

print()
print(len(todos) - falhas, "de", len(todos), "testes passaram")
