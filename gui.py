"""
gui.py - Interface gráfica (Tkinter) para o Sistema de Busca em Documentos.
Reaproveita as estruturas do main.py (Trie + índice invertido) e o kmp.py.
Execute com: python gui.py
"""
import os
import time
import re
import tkinter as tk
from tkinter import ttk, messagebox

# Garante que "documentos/" e "stopwords.txt" sejam encontrados
# mesmo que o programa seja aberto a partir de outra pasta.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from main import construir_estruturas
from indice_invertido import consultar_palavra
from kmp import buscar_sequencia_nos_documentos


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
        abas.add(self._aba_adicionar(), text="Adicionar documento")
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

    def _aba_adicionar(self):
        frame = ttk.Frame(self, padding=10)

        linha = ttk.Frame(frame)
        linha.pack(fill="x")
        ttk.Label(linha, text="Nome do arquivo:").pack(side="left")
        self.entrada_nome = ttk.Entry(linha)
        self.entrada_nome.pack(side="left", fill="x", expand=True, padx=8)
        ttk.Label(linha, text=".txt").pack(side="left")

        ttk.Label(frame, text="Conteúdo do documento:").pack(anchor="w", pady=(10, 0))
        self.texto_novo = tk.Text(frame, wrap="word", font=("Consolas", 10), height=10)
        self.texto_novo.pack(fill="both", expand=True, pady=(4, 0))

        ttk.Button(frame, text="Salvar e reindexar",
                   command=self.adicionar_documento).pack(anchor="e", pady=(10, 0))
        return frame

    def _aba_documentos(self):
        frame = ttk.Frame(self, padding=10)
        self.rotulo_documentos = ttk.Label(frame)
        self.rotulo_documentos.pack(anchor="w")
        self.lista_documentos = tk.Listbox(frame, font=("Consolas", 10))
        self.lista_documentos.pack(fill="both", expand=True, pady=(8, 0))
        self._atualizar_documentos()
        return frame

    def _atualizar_documentos(self):
        nomes = self.estatisticas["nomes_documentos"]
        self.rotulo_documentos.configure(text=f"Documentos processados ({len(nomes)}):")
        self.lista_documentos.delete(0, "end")
        for nome in sorted(nomes):
            self.lista_documentos.insert("end", nome)

    def _aba_estatisticas(self):
        frame = ttk.Frame(self, padding=10)
        nomes = ["Documentos processados", "Total de palavras", "Termos distintos",
                 "Tempo de construção da Trie", "Tempo de construção do índice invertido"]
        self.valores_estatisticas = []
        for linha, nome in enumerate(nomes):
            valor = tk.StringVar()
            self.valores_estatisticas.append(valor)
            ttk.Label(frame, text=nome + ":").grid(row=linha, column=0, sticky="w", pady=4)
            ttk.Label(frame, textvariable=valor, font=("Segoe UI", 10, "bold")).grid(
                row=linha, column=1, sticky="w", padx=12)
        self._atualizar_estatisticas()
        return frame

    def _atualizar_estatisticas(self):
        e = self.estatisticas
        dados = [e["documentos_processados"], e["total_palavras"], e["termos_distintos"],
                 f"{e['tempo_trie']:.6f} s", f"{e['tempo_indice']:.6f} s"]
        for var, valor in zip(self.valores_estatisticas, dados):
            var.set(str(valor))

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
                partes.extend(f"    ...{t}..." for t in d["trechos"])
            texto = "\n".join(partes)
        else:
            texto = "Sequência não encontrada em nenhum documento."
        self._mostrar(saida, texto, tempo)

    def adicionar_documento(self):
        nome = self.entrada_nome.get().strip()
        if nome.lower().endswith(".txt"):
            nome = nome[:-4]
        nome = re.sub(r'[\\/:*?"<>|]', "", nome).strip()  # remove caracteres inválidos
        conteudo = self.texto_novo.get("1.0", "end").strip()

        if not nome:
            messagebox.showwarning("Atenção", "Informe um nome para o arquivo.")
            return
        if not conteudo:
            messagebox.showwarning("Atenção", "O conteúdo do documento está vazio.")
            return

        arquivo = nome + ".txt"
        caminho = os.path.join("documentos", arquivo)
        if os.path.exists(caminho) and not messagebox.askyesno(
                "Arquivo existente", f'"{arquivo}" já existe. Deseja substituí-lo?'):
            return

        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)

        # Reconstrói a Trie e o índice invertido com o novo documento
        termos_antes = self.estatisticas["termos_distintos"]
        self.trie, self.indice, self.estatisticas = construir_estruturas()
        novos = self.estatisticas["termos_distintos"] - termos_antes

        self._atualizar_documentos()
        self._atualizar_estatisticas()
        self.entrada_nome.delete(0, "end")
        self.texto_novo.delete("1.0", "end")
        self.status.configure(text=f'"{arquivo}" salvo e indexado. '
                                   f'Termos distintos novos: {novos}')


if __name__ == "__main__":
    App().mainloop()