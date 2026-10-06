"""
gui.py - Interface gráfica (Tkinter) para o Sistema de Busca em Documentos.
Reaproveita as estruturas do main.py (Trie + índice invertido) e o kmp.py.
Execute com: python gui.py
"""
import os
import time
import tkinter as tk
from tkinter import ttk

# Garante que "documentos/" e "stopwords.txt" sejam encontrados
# mesmo que o programa seja aberto a partir de outra pasta.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from main import construir_estruturas
from indice_invertido import consultar_palavra
from kmp import buscar_sequencia_nos_documentos, _trecho


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Busca em Documentos")
        self.geometry("720x480")
        self.minsize(560, 380)

        self.trie, self.indice, self.estatisticas = construir_estruturas()

        abas = ttk.Notebook(self)
        abas.pack(fill="both", expand=True, padx=10, pady=10)

        abas.add(self._aba_busca("Digite a palavra:", self.buscar_palavra), text="Buscar palavra")
        abas.add(self._aba_busca("Digite o prefixo:", self.buscar_prefixo, ao_digitar=True), text="Buscar por prefixo")
        abas.add(self._aba_busca("Digite a sequência:", self.buscar_sequencia), text="Buscar sequência (KMP)")
        abas.add(self._aba_documentos(), text="Documentos")
        abas.add(self._aba_estatisticas(), text="Estatísticas")

        self.status = ttk.Label(self, text="Pronto.", anchor="w")
        self.status.pack(fill="x", padx=10, pady=(0, 8))

    # ---------- construção das abas ----------

    def _aba_busca(self, rotulo, acao, ao_digitar=False):
        frame = ttk.Frame(self, padding=10)

        linha = ttk.Frame(frame)
        linha.pack(fill="x")
        ttk.Label(linha, text=rotulo).pack(side="left")
        entrada = ttk.Entry(linha)
        entrada.pack(side="left", fill="x", expand=True, padx=8)
        botao = ttk.Button(linha, text="Buscar")
        botao.pack(side="left")

        saida = tk.Text(frame, wrap="word", state="disabled", font=("Consolas", 10))
        barra = ttk.Scrollbar(frame, command=saida.yview)
        saida.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y", pady=(10, 0))
        saida.pack(fill="both", expand=True, pady=(10, 0))

        executar = lambda *_: acao(entrada.get(), saida)
        botao.configure(command=executar)
        entrada.bind("<Return>", executar)
        if ao_digitar:  # autocomplete: atualiza a cada tecla
            entrada.bind("<KeyRelease>", executar)
        return frame

    def _aba_documentos(self):
        frame = ttk.Frame(self, padding=10)
        nomes = self.estatisticas["nomes_documentos"]
        ttk.Label(frame, text=f"Documentos processados ({len(nomes)}):").pack(anchor="w")
        lista = tk.Listbox(frame, font=("Consolas", 10))
        lista.pack(fill="both", expand=True, pady=(8, 0))
        for nome in sorted(nomes):
            lista.insert("end", nome)
        return frame

    def _aba_estatisticas(self):
        frame = ttk.Frame(self, padding=10)
        e = self.estatisticas
        dados = [
            ("Documentos processados", e["documentos_processados"]),
            ("Total de palavras", e["total_palavras"]),
            ("Termos distintos", e["termos_distintos"]),
            ("Tempo de construção da Trie", f"{e['tempo_trie']:.6f} s"),
            ("Tempo de construção do índice invertido", f"{e['tempo_indice']:.6f} s"),
        ]
        for linha, (nome, valor) in enumerate(dados):
            ttk.Label(frame, text=nome + ":").grid(row=linha, column=0, sticky="w", pady=4)
            ttk.Label(frame, text=str(valor), font=("Segoe UI", 10, "bold")).grid(
                row=linha, column=1, sticky="w", padx=12)
        return frame

    # ---------- ações ----------

    def _mostrar(self, saida, texto, tempo):
        saida.configure(state="normal")
        saida.delete("1.0", "end")
        saida.insert("1.0", texto)
        saida.configure(state="disabled")
        self.status.configure(text=f"Consulta levou {tempo:.6f} segundos")

    def buscar_palavra(self, palavra, saida):
        palavra = palavra.strip().lower()
        if not palavra:
            return
        inicio = time.perf_counter()
        documentos = consultar_palavra(self.indice, palavra)
        tempo = time.perf_counter() - inicio

        if documentos:
            texto = f"Encontrada em {len(documentos)} arquivo(s):\n"
            texto += "\n".join(f"  - {doc}" for doc in sorted(documentos))
        else:
            texto = "Palavra não encontrada em nenhum documento."
        self._mostrar(saida, texto, tempo)

    def buscar_prefixo(self, prefixo, saida):
        prefixo = prefixo.strip().lower()
        if not prefixo:
            self._mostrar(saida, "", 0)
            return
        inicio = time.perf_counter()
        palavras = self.trie.buscar_prefixo(prefixo)
        resultado = {p: consultar_palavra(self.indice, p) for p in palavras}
        tempo = time.perf_counter() - inicio

        if resultado:
            texto = f"{len(resultado)} palavra(s) encontrada(s):\n"
            texto += "\n".join(f"  {p} -> {', '.join(sorted(d))}" for p, d in sorted(resultado.items()))
        else:
            texto = "Nenhuma palavra encontrada com esse prefixo."
        self._mostrar(saida, texto, tempo)

    def buscar_sequencia(self, padrao, saida):
        if not padrao:
            return
        resultados, tempo = buscar_sequencia_nos_documentos("documentos", padrao)

        if resultados:
            partes = [f"Encontrada em {len(resultados)} arquivo(s):"]
            for nome, d in resultados.items():
                partes.append(f"\n- {nome} ({d['total']} ocorrência(s))")
                original = open(os.path.join("documentos", nome), encoding="utf-8").read()
                partes.extend(f"    ...{_trecho(original, p, len(padrao))}..." for p in d["posicoes"])
            texto = "\n".join(partes)
        else:
            texto = "Sequência não encontrada em nenhum documento."
        self._mostrar(saida, texto, tempo)


if __name__ == "__main__":
    App().mainloop()
