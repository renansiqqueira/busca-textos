import re
import os


def carregar_stopwords(caminho="stopwords.txt"):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return set(linha.strip().lower() for linha in arquivo if linha.strip())


def limpar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto


def tokenizar(texto):
    return texto.split()


def remover_stopwords(tokens, stopwords):
    return [token for token in tokens if token not in stopwords]


def processar_texto(texto, stopwords):
    texto_limpo = limpar_texto(texto)
    tokens = tokenizar(texto_limpo)
    return remover_stopwords(tokens, stopwords)


def processar_pasta(caminho_pasta, stopwords):
    arquivos_processados = {}
    for nome_arquivo in os.listdir(caminho_pasta):
        if nome_arquivo.endswith(".txt"):
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
            with open(caminho_completo, "r", encoding="utf-8") as arquivo:
                texto = arquivo.read()
            arquivos_processados[nome_arquivo] = processar_texto(texto, stopwords)
    return arquivos_processados


if __name__ == "__main__":
    stopwords = carregar_stopwords()
    resultado = processar_pasta("documentos", stopwords)
    for nome, tokens in resultado.items():
        print(f"{nome}: {len(tokens)} palavras -> {tokens[:10]}...")