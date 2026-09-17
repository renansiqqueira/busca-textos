class NoTrie:
    def __init__(self):
        self.filhos = {}
        self.fim_de_palavra = False

class Trie:
    def __init__(self):
        self.raiz = NoTrie()

    def inserir(self, palavra):
        no_atual = self.raiz
        for letra in palavra:
            if letra not in no_atual.filhos:
                no_atual.filhos[letra] = NoTrie()
            no_atual = no_atual.filhos[letra]
        no_atual.fim_de_palavra = True

    def buscar(self, palavra):
        no_atual = self.raiz
        for letra in palavra:
            if letra not in no_atual.filhos:
                return False
            no_atual = no_atual.filhos[letra]
        return no_atual.fim_de_palavra
    
    def _no_do_prefixo(self, prefixo):
        no_atual = self.raiz
        for letra in prefixo:
            if letra not in no_atual.filhos:
                return None
            no_atual = no_atual.filhos[letra]
        return no_atual

    def buscar_prefixo(self, prefixo):
        no_prefixo = self._no_do_prefixo(prefixo)
        if no_prefixo is None:
            return []

        resultados = []

        def coletar(no, caminho):
            if no.fim_de_palavra:
                resultados.append(caminho)
            for letra, filho in no.filhos.items():
                coletar(filho, caminho + letra)

        coletar(no_prefixo, prefixo)
        return resultados


if __name__ == "__main__":
    trie = Trie()
    palavras_iniciais = ["computador", "computação", "computacional",
                         "compilador", "complexidade", "programação",
                         "processador", "processamento"]
    for palavra in palavras_iniciais:
        trie.inserir(palavra)

    while True:
        print("\n====================================")
        print(" AUTOCOMPLETE COM TRIE")
        print("====================================")
        print("1 - Buscar palavra")
        print("2 - Buscar por prefixo")
        print("3 - Inserir nova palavra")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            palavra = input("Digite a palavra: ")
            if trie.buscar(palavra):
                print(f'"{palavra}" existe na Trie.')
            else:
                print(f'"{palavra}" não foi encontrada.')

        elif opcao == "2":
            prefixo = input("Digite o prefixo: ")
            resultados = trie.buscar_prefixo(prefixo)
            if resultados:
                print("Palavras encontradas:")
                for palavra in sorted(resultados):
                    print(f"  {palavra}")
            else:
                print("Nenhuma palavra encontrada com esse prefixo.")

        elif opcao == "3":
            nova = input("Digite a nova palavra: ")
            trie.inserir(nova)
            print(f'"{nova}" foi inserida.')

        elif opcao == "4":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")