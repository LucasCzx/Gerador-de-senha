# Testes do gerador de senhas
# Para rodar: python test_gerador_senha.py

import hashlib
import os

import gerador_senha as g

# Guarda o valor real de segurança antes de diminuir só para os testes
iteracoes_de_verdade = g.ITERACOES

# Nos testes usamos poucas repetições só pra eles rodarem rápido
g.ITERACOES = 1000

arquivo_teste = "registro_teste.txt"
salt_a = "aa" * 16
salt_b = "bb" * 16


def apagar_arquivo(nome):
    if os.path.exists(nome):
        os.remove(nome)


# ---------- criando as senhas ----------

def teste_tamanho_correto():
    for tamanho in [12, 16, 20, 64]:
        assert len(g.gerar_senha(tamanho)) == tamanho


def teste_tamanho_minimo():
    # Se pedirem menos que 12, o programa entrega 12
    assert len(g.gerar_senha(3)) == 12


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


# ---------- nunca repetir senha ----------

def teste_senhas_nunca_repetem():
    apagar_arquivo(arquivo_teste)
    senhas = []
    for i in range(200):
        senhas.append(g.gerar_senha_unica(12, arquivo_teste))

    assert len(set(senhas)) == 200                    # nenhuma repetida
    assert len(g.ler_registro(arquivo_teste)) == 200  # todas registradas
    apagar_arquivo(arquivo_teste)


def teste_senhas_unicas_sem_padrao_facil():
    apagar_arquivo(arquivo_teste)
    for i in range(100):
        senha = g.gerar_senha_unica(12, arquivo_teste)
        assert g.tem_padrao_facil(senha) == False
    apagar_arquivo(arquivo_teste)


def teste_conflito_e_evitado():
    # Aqui a gente força o gerador a sortear a mesma senha duas vezes,
    # pra ver se ele percebe e tenta de novo
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
        g.gerar_senha = original  # devolve a função de verdade
        apagar_arquivo(arquivo_teste)

    assert primeira == "Aq7#mK!x2Zp9"
    assert segunda == "Bw4$nR&y8Lc3"   # a repetida foi descartada


# ---------- segurança do registro ----------

def teste_registro_nao_guarda_a_senha():
    apagar_arquivo(arquivo_teste)
    senha = g.gerar_senha_unica(12, arquivo_teste)

    with open(arquivo_teste, "r", encoding="utf-8") as f:
        conteudo = f.read()
    apagar_arquivo(arquivo_teste)

    hash_simples = hashlib.sha256(senha.encode("utf-8")).hexdigest()

    assert senha not in conteudo          # a senha não aparece
    assert hash_simples not in conteudo   # nem o hash simples dela


def teste_codigo_depende_do_salt():
    senha = "Aq7#mK!x2Zp9"
    # Mesma senha e mesmo salt: sempre o mesmo código
    assert g.criar_codigo(senha, salt_a) == g.criar_codigo(senha, salt_a)
    # Salts diferentes: códigos diferentes
    assert g.criar_codigo(senha, salt_a) != g.criar_codigo(senha, salt_b)


def teste_salt_e_criado_uma_vez():
    apagar_arquivo(arquivo_teste)
    primeiro = g.garantir_salt(arquivo_teste)
    segundo = g.garantir_salt(arquivo_teste)
    apagar_arquivo(arquivo_teste)

    assert primeiro == segundo
    assert len(primeiro) == 32


def teste_cada_instalacao_tem_salt_diferente():
    outro = "registro_teste2.txt"
    apagar_arquivo(arquivo_teste)
    apagar_arquivo(outro)
    salt1 = g.garantir_salt(arquivo_teste)
    salt2 = g.garantir_salt(outro)
    apagar_arquivo(arquivo_teste)
    apagar_arquivo(outro)

    assert salt1 != salt2


def teste_registro_ignora_comentarios_e_salt():
    apagar_arquivo(arquivo_teste)
    g.garantir_salt(arquivo_teste)
    g.salvar_no_registro("abc123", arquivo_teste)
    g.salvar_no_registro("def456", arquivo_teste)

    with open(arquivo_teste, "r", encoding="utf-8") as f:
        primeira_linha = f.readline()
    codigos = g.ler_registro(arquivo_teste)
    apagar_arquivo(arquivo_teste)

    assert primeira_linha.startswith("#")
    assert codigos == ["abc123", "def456"]   # sem comentários e sem o salt


def teste_registro_so_o_dono_le():
    if os.name == "nt":
        return  # no Windows essa permissão funciona de outro jeito

    apagar_arquivo(arquivo_teste)
    g.salvar_no_registro("abc123", arquivo_teste)
    permissao = os.stat(arquivo_teste).st_mode & 0o777
    apagar_arquivo(arquivo_teste)

    assert permissao == 0o600


def teste_registro_fica_fora_da_pasta_do_programa():
    pasta_programa = os.path.dirname(os.path.abspath(g.__file__))
    pasta_registro = os.path.dirname(os.path.abspath(g.ARQUIVO_REGISTRO))
    assert pasta_registro != pasta_programa
    assert not pasta_registro.startswith(pasta_programa)


def teste_iteracoes_de_verdade_sao_altas():
    assert iteracoes_de_verdade >= 100000


def teste_programa_nao_salva_senhas():
    # Garantia pro futuro: ninguém pode colocar de volta uma função
    # que grave a senha em arquivo
    assert not hasattr(g, "salvar_senha_em_arquivo")
    assert not hasattr(g, "oferecer_salvar")


todos = [teste_tamanho_correto, teste_tamanho_minimo,
         teste_tem_todos_os_tipos, teste_padroes_faceis,
         teste_senhas_nunca_repetem, teste_senhas_unicas_sem_padrao_facil,
         teste_conflito_e_evitado, teste_registro_nao_guarda_a_senha,
         teste_codigo_depende_do_salt, teste_salt_e_criado_uma_vez,
         teste_cada_instalacao_tem_salt_diferente,
         teste_registro_ignora_comentarios_e_salt, teste_registro_so_o_dono_le,
         teste_registro_fica_fora_da_pasta_do_programa,
         teste_iteracoes_de_verdade_sao_altas, teste_programa_nao_salva_senhas]

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
