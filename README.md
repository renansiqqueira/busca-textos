# Sistema de Busca em Documentos com Trie e Índice Invertido

Trabalho Prático (A1) — Unidade 2 — Análise e Otimização de Sistemas — UVA

**Equipe:** Leonardo Salgado, Renan Siqueira e Vinicius Lima

## Sobre o projeto
Sistema que lê arquivos `.txt`, processa o texto e permite buscas rápidas usando três estruturas/algoritmos:

- **Índice invertido** (tabela hash): descobre em quais documentos uma palavra aparece, em O(1) no caso médio.
- **Trie**: busca por prefixo (autocomplete), com custo proporcional ao tamanho do prefixo.
- **KMP (Knuth-Morris-Pratt)**: busca uma sequência de caracteres no texto original dos documentos, em O(n + m).

O sistema pode ser usado pelo terminal ou por uma interface gráfica.

## Requisitos
- Python 3.10 ou superior
- Não usa bibliotecas externas. A interface gráfica usa o **Tkinter**, que já vem com o Python no Windows e no macOS.
  No Linux, pode ser necessário instalar: `sudo apt install python3-tk`

## Estrutura do projeto
```
projeto/
├── documentos/            # arquivos .txt processados automaticamente
├── preprocessamento.py    # limpeza, tokenização e remoção de stopwords
├── indice_invertido.py    # vocabulário e índice invertido (hash)
├── trie.py                # estrutura Trie (Parte I)
├── kmp.py                 # busca de sequência com o algoritmo KMP
├── main.py                # construção das estruturas, menu no terminal e estatísticas
├── gui.py                 # interface gráfica (Tkinter)
└── stopwords.txt          # lista de stopwords em português
```

## Como executar
1. Coloque os arquivos `.txt` desejados dentro da pasta `documentos/`
2. Escolha uma das formas de uso:

**Interface gráfica (recomendado)**
```
python gui.py
```
A janela possui seis abas:
- **Buscar palavra**: mostra os documentos em que a palavra aparece (índice invertido)
- **Buscar por prefixo**: lista as palavras que começam com o prefixo e seus documentos, atualizando a cada tecla (Trie)
- **Buscar sequência (KMP)**: procura a sequência no texto original e mostra trechos de contexto
- **Adicionar documento**: cria um novo `.txt` na pasta `documentos/` a partir de um nome e de um texto digitado, e reconstrói a Trie e o índice invertido na hora
- **Documentos**: lista os arquivos processados
- **Estatísticas**: total de documentos, palavras, termos distintos e tempos de construção das estruturas

O tempo de cada consulta aparece no rodapé da janela.

**Terminal**
```
python main.py
```
Menu com as opções de buscar palavra, buscar por prefixo, listar documentos e exibir estatísticas.

## Testes individuais dos módulos
Cada módulo pode ser executado sozinho para testes:

| Comando | O que faz |
|---|---|
| `python trie.py` | Menu de autocomplete com a Trie isolada (Parte I) |
| `python preprocessamento.py` | Mostra os tokens gerados de cada documento |
| `python indice_invertido.py` | Mostra o tamanho do vocabulário e um exemplo de consulta |
| `python kmp.py` | Busca de sequência pelo terminal |

## Observação
Novos arquivos `.txt` adicionados à pasta `documentos/` são processados automaticamente na próxima execução, sem necessidade de alterar o código. Pela interface gráfica, a aba **Adicionar documento** faz isso sem precisar reiniciar o programa.