# Sistema de Busca em Documentos com Trie e Índice Invertido

Trabalho Prático (A1) — Unidade 2 — Análise e Otimização de Sistemas — UVA

## Requisitos
- Python 3.10 ou superior (não usa bibliotecas externas)

## Estrutura do projeto
projeto/
├── documentos/ # arquivos .txt processados automaticamente
├── trie.py # estrutura Trie (Parte I)
├── preprocessamento.py # limpeza, tokenização e stopwords
├── indice_invertido.py # vocabulário e índice invertido (hash)
├── main.py # menu principal e estatísticas
└── stopwords.txt # lista de stopwords em português

## Como executar
1. Coloque os arquivos `.txt` desejados dentro da pasta `documentos/`
2. Rode `python main.py`
3. Use o menu para buscar palavras, buscar por prefixo, listar documentos e ver estatísticas

## Observação
Novos arquivos `.txt` adicionados à pasta `documentos/` são processados automaticamente na próxima execução — não é necessário alterar o código.