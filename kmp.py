"""
kmp.py - Desafio opcional (tópico 9): busca de sequência de caracteres
diretamente no conteúdo ORIGINAL dos documentos, usando o algoritmo KMP
(Knuth-Morris-Pratt).

Complexidade:
  - Pré-processamento (tabela de prefixos / LPS): O(m)
  - Busca no texto:                               O(n)
  - Total por documento:                          O(n + m)
  (n = tamanho do texto, m = tamanho do padrão)
  Comparado à busca ingênua O(n * m) no pior caso, o KMP nunca "volta"
  no texto: o índice i só avança.
"""
import os
import time


def construir_lps(padrao):
    """
    Constrói a tabela LPS (Longest Proper Prefix which is also Suffix).
    lps[i] = tamanho do maior prefixo próprio de padrao[:i+1] que também
    é sufixo dele. Custo: O(m).
    """
    m = len(padrao)
    lps = [0] * m
    k = 0  # tamanho do prefixo-sufixo atual
    for i in range(1, m):
        while k > 0 and padrao[i] != padrao[k]:
            k = lps[k - 1]          # recua usando a própria tabela
        if padrao[i] == padrao[k]:
            k += 1
        lps[i] = k
    return lps


def kmp_busca(texto, padrao):
    """
    Retorna a lista com os índices iniciais de TODAS as ocorrências
    (inclusive sobrepostas) de `padrao` em `texto`. Custo: O(n + m).
    """
    n, m = len(texto), len(padrao)
    if m == 0 or m > n:
        return []
    lps = construir_lps(padrao)
    ocorrencias = []
    j = 0  # posição atual no padrão
    for i in range(n):              # i nunca retrocede
        while j > 0 and texto[i] != padrao[j]:
            j = lps[j - 1]          # desliza o padrão sem reler o texto
        if texto[i] == padrao[j]:
            j += 1
        if j == m:                  # casamento completo
            ocorrencias.append(i - m + 1)
            j = lps[j - 1]          # permite ocorrências sobrepostas
    return ocorrencias


def _trecho(texto, pos, tam, margem=30):
    """Recorta um trecho de contexto ao redor da ocorrência."""
    ini = max(0, pos - margem)
    fim = min(len(texto), pos + tam + margem)
    return texto[ini:fim].replace("\n", " ").strip()


def buscar_sequencia_nos_documentos(pasta, padrao, ignorar_maiusculas=True):
    """
    Procura `padrao` no conteúdo original de todos os .txt da pasta
    (nomes não fixados no código). Retorna (resultados, tempo_segundos),
    onde resultados = {arquivo: {"total": int, "posicoes": [...], "trechos": [...]}}
    contendo apenas os arquivos em que a sequência aparece.
    """
    inicio = time.perf_counter()
    resultados = {}
    alvo = padrao.lower() if ignorar_maiusculas else padrao

    for nome in sorted(os.listdir(pasta)):
        if not nome.lower().endswith(".txt"):
            continue
        with open(os.path.join(pasta, nome), encoding="utf-8") as f:
            original = f.read()
        texto = original.lower() if ignorar_maiusculas else original
        pos = kmp_busca(texto, alvo)
        if pos:
            resultados[nome] = {
                "total": len(pos),
                "posicoes": pos,
                "trechos": [_trecho(original, p, len(alvo)) for p in pos[:3]],
            }
    return resultados, time.perf_counter() - inicio


def menu_busca_sequencia(pasta="documentos"):
    """Opção 3 do menu: 'Buscar sequência nos documentos (opcional)'."""
    padrao = input("Digite a sequência de caracteres: ")
    if not padrao:
        print("Sequência vazia.")
        return
    res, tempo = buscar_sequencia_nos_documentos(pasta, padrao)
    if not res:
        print("Sequência não encontrada em nenhum documento.")
    else:
        print(f"Encontrada em {len(res)} arquivo(s):")
        for nome, d in res.items():
            print(f"- {nome} ({d['total']} ocorrência(s))")
            for t in d["trechos"]:
                print(f"    ...{t}...")
    print(f"Tempo da consulta: {tempo * 1000:.3f} ms")


if __name__ == "__main__":
    menu_busca_sequencia()
