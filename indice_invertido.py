def construir_vocabulario(arquivos_processados):
    vocabulario = set()
    for tokens in arquivos_processados.values():
        vocabulario.update(tokens)
    return vocabulario


def construir_indice_invertido(arquivos_processados):
    indice = {}
    for nome_arquivo, tokens in arquivos_processados.items():
        for palavra in tokens:
            if palavra not in indice:
                indice[palavra] = set()
            indice[palavra].add(nome_arquivo)
    return indice


def consultar_palavra(indice_invertido, palavra):
    return indice_invertido.get(palavra, set())


if __name__ == "__main__":
    from preprocessamento import carregar_stopwords, processar_pasta

    stopwords = carregar_stopwords()
    arquivos_processados = processar_pasta("documentos", stopwords)

    vocabulario = construir_vocabulario(arquivos_processados)
    indice = construir_indice_invertido(arquivos_processados)

    print(f"Vocabulário: {len(vocabulario)} termos distintos")
    print(f"Documentos com 'algoritmo': {consultar_palavra(indice, 'algoritmo')}")