import time
from trie import Trie
from preprocessamento import carregar_stopwords, processar_pasta
from indice_invertido import construir_vocabulario, construir_indice_invertido, consultar_palavra


def construir_estruturas():
    stopwords = carregar_stopwords()
    arquivos_processados = processar_pasta("documentos", stopwords)

    total_palavras = sum(len(tokens) for tokens in arquivos_processados.values())
    vocabulario = construir_vocabulario(arquivos_processados)

    inicio_indice = time.perf_counter()
    indice = construir_indice_invertido(arquivos_processados)
    tempo_indice = time.perf_counter() - inicio_indice

    inicio_trie = time.perf_counter()
    trie = Trie()
    for palavra in vocabulario:
        trie.inserir(palavra)
    tempo_trie = time.perf_counter() - inicio_trie

    estatisticas = {
        "documentos_processados": len(arquivos_processados),
        "nomes_documentos": list(arquivos_processados.keys()),
        "total_palavras": total_palavras,
        "termos_distintos": len(vocabulario),
        "tempo_trie": tempo_trie,
        "tempo_indice": tempo_indice,
    }

    return trie, indice, estatisticas


def exibir_menu():
    print("\n================================================")
    print(" SISTEMA DE BUSCA EM DOCUMENTOS")
    print("================================================")
    print("1 - Buscar palavra")
    print("2 - Buscar por prefixo")
    print("3 - Listar documentos")
    print("4 - Exibir estatísticas")
    print("5 - Sair")


def main():
    trie, indice, estatisticas = construir_estruturas()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            palavra = input("Digite a palavra: ").lower()
            inicio = time.perf_counter()
            documentos = consultar_palavra(indice, palavra)
            tempo = time.perf_counter() - inicio

            if documentos:
                print(f"Encontrada em {len(documentos)} arquivo(s):")
                for doc in sorted(documentos):
                    print(f"  - {doc}")
            else:
                print("Palavra não encontrada em nenhum documento.")
            print(f"(consulta levou {tempo:.6f} segundos)")

        elif opcao == "2":
            prefixo = input("Digite o prefixo: ").lower()
            inicio = time.perf_counter()
            palavras_encontradas = trie.buscar_prefixo(prefixo)
            resultado = {p: consultar_palavra(indice, p) for p in palavras_encontradas}
            tempo = time.perf_counter() - inicio

            if resultado:
                print("Palavras encontradas:")
                for palavra, docs in sorted(resultado.items()):
                    print(f"  {palavra} -> {sorted(docs)}")
            else:
                print("Nenhuma palavra encontrada com esse prefixo.")
            print(f"(consulta levou {tempo:.6f} segundos)")

        elif opcao == "3":
            print(f"Documentos processados ({estatisticas['documentos_processados']}):")
            for nome in estatisticas["nomes_documentos"]:
                print(f"  - {nome}")

        elif opcao == "4":
            print("Estatísticas:")
            print(f"  Documentos processados: {estatisticas['documentos_processados']}")
            print(f"  Total de palavras: {estatisticas['total_palavras']}")
            print(f"  Termos distintos: {estatisticas['termos_distintos']}")
            print(f"  Tempo de construção da Trie: {estatisticas['tempo_trie']:.6f}s")
            print(f"  Tempo de construção do índice invertido: {estatisticas['tempo_indice']:.6f}s")

        elif opcao == "5":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()