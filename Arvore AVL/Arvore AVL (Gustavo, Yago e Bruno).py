import tkinter as tk
from tkinter import Canvas
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle
import os
import time

class No:
    def __init__(self, chave):
        self.esquerda = None
        self.direita = None
        self.valor = chave
        self.altura = 1

class ArvoreAVL:
    def __init__(self, interface):
        self.raiz = None
        self.interface = interface

    def inserir(self, chave):
        self.raiz = self._inserir(self.raiz, chave)

    def _inserir(self, no, chave):
        # Caso base: se o nó é None, cria um novo nó
        if no is None:
            return No(chave)
        elif chave < no.valor:
            no.esquerda = self._inserir(no.esquerda, chave)
        elif chave > no.valor:
            no.direita = self._inserir(no.direita, chave)
        else:
            return no  # Evita a inserção de valores duplicados

        # Atualiza a altura do nó atual
        no.altura = 1 + max(self.obter_altura(no.esquerda), self.obter_altura(no.direita))
        balanceamento = self.calcular_balanceamento(no)

        # Rotação à Direita
        if balanceamento > 1 and chave < no.esquerda.valor:
            self.interface.exibir_rotacao(no, no.esquerda, "Rotação à Direita")
            return self.rotacionar_direita(no)

        # Rotação à Esquerda
        if balanceamento < -1 and chave > no.direita.valor:
            self.interface.exibir_rotacao(no, no.direita, "Rotação à Esquerda")
            return self.rotacionar_esquerda(no)

        # Rotação Dupla (Esquerda-Direita)
        if balanceamento > 1 and chave > no.esquerda.valor:
            no.esquerda = self.rotacionar_esquerda(no.esquerda)
            self.interface.exibir_rotacao(no, no.esquerda, "Rotação Dupla à direita")
            return self.rotacionar_direita(no)

        # Rotação Dupla (Direita-Esquerda)
        if balanceamento < -1 and chave < no.direita.valor:
            no.direita = self.rotacionar_direita(no.direita)
            self.interface.exibir_rotacao(no, no.direita, "Rotação à esquerda")
            return self.rotacionar_esquerda(no)

        return no

    def remover(self, chave):
        self.raiz = self._remover(self.raiz, chave)

    def _remover(self, no, chave):
        if not no:
            return no
        elif chave < no.valor:
            no.esquerda = self._remover(no.esquerda, chave)
        elif chave > no.valor:
            no.direita = self._remover(no.direita, chave)
        else:
            # Caso com apenas um filho ou nenhum filho
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda

            # Caso com dois filhos
            menor_no_maior_subarvore = self._minimo_valor_no(no.direita)
            no.valor = menor_no_maior_subarvore.valor
            no.direita = self._remover(no.direita, menor_no_maior_subarvore.valor)

        # Atualiza a altura do nó atual
        no.altura = 1 + max(self.obter_altura(no.esquerda), self.obter_altura(no.direita))
        balanceamento = self.calcular_balanceamento(no)

        # Rotação à Direita
        if balanceamento > 1 and self.calcular_balanceamento(no.esquerda) >= 0:
            self.interface.exibir_rotacao(no, no.esquerda, "Rotação à Direita")
            return self.rotacionar_direita(no)

        # Rotação Dupla (Esquerda-Direita)
        if balanceamento > 1 and self.calcular_balanceamento(no.esquerda) < 0:
            no.esquerda = self.rotacionar_esquerda(no.esquerda)
            self.interface.exibir_rotacao(no, no.esquerda, "Rotação à Direita")
            return self.rotacionar_direita(no)

        # Rotação à Esquerda
        if balanceamento < -1 and self.calcular_balanceamento(no.direita) <= 0:
            self.interface.exibir_rotacao(no, no.direita, "Rotação à Esquerda")
            return self.rotacionar_esquerda(no)

        # Rotação Dupla (Direita-Esquerda)
        if balanceamento < -1 and self.calcular_balanceamento(no.direita) > 0:
            no.direita = self.rotacionar_direita(no.direita)
            self.interface.exibir_rotacao(no, no.direita, "Rotação à Esquerda")
            return self.rotacionar_esquerda(no)

        return no

    def _minimo_valor_no(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def obter_altura(self, no):
        if not no:
            return 0
        return no.altura

    def calcular_balanceamento(self, no):
        if not no:
            return 0
        return self.obter_altura(no.esquerda) - self.obter_altura(no.direita)

    def rotacionar_direita(self, z):
        y = z.esquerda
        T3 = y.direita
        y.direita = z
        z.esquerda = T3
        # Atualiza a altura dos nós envolvidos na rotação
        z.altura = 1 + max(self.obter_altura(z.esquerda), self.obter_altura(z.direita))
        y.altura = 1 + max(self.obter_altura(y.esquerda), self.obter_altura(y.direita))
        return y

    def rotacionar_esquerda(self, z):
        y = z.direita
        T2 = y.esquerda
        y.esquerda = z
        z.direita = T2
        # Atualiza a altura dos nós envolvidos na rotação
        z.altura = 1 + max(self.obter_altura(z.esquerda), self.obter_altura(z.direita))
        y.altura = 1 + max(self.obter_altura(y.esquerda), self.obter_altura(y.direita))
        return y

    def salvar_arvore(self, caminho_arquivo):
        with open(caminho_arquivo, 'wb') as arquivo:
            pickle.dump(self.raiz, arquivo)

    def carregar_arvore(self, caminho_arquivo):
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'rb') as arquivo:
                self.raiz = pickle.load(arquivo)

    def resetar_arvore(self):
        self.raiz = None

class InterfaceArvoreAVL:
    def __init__(self):
        self.caminho_arquivo = 'arvore_avl.bin'
        self.arvore = ArvoreAVL(self)
        self.arvore.carregar_arvore(self.caminho_arquivo)

        self.janela = tk.Tk()
        self.janela.title("Árvore AVL")

        self.canvas = Canvas(self.janela, width=800, height=600)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.entrada = tk.Entry(self.janela)
        self.entrada.grid(row=1, column=0, padx=1, pady=1)

        self.botao_adicionar = tk.Button(self.janela, text="Adicionar Nó", command=self.adicionar_no)
        self.botao_adicionar.grid(row=1, column=1, padx=1, pady=1)

        self.botao_remover = tk.Button(self.janela, text="Remover Nó", command=self.remover_no)
        self.botao_remover.grid(row=1, column=2, padx=1, pady=1)

        self.botao_resetar = tk.Button(self.janela, text="Resetar Árvore", command=self.resetar_arvore)
        self.botao_resetar.grid(row=2, column=2, padx=1, pady=1)

        self.canvas_figura_agg = None

        self.desenhar_arvore()

        self.janela.protocol("WM_DELETE_WINDOW", self.salvar_e_sair)

        self.janela.mainloop()

    def adicionar_no(self):
        chave = int(self.entrada.get())
        self.arvore.inserir(chave)
        self.desenhar_arvore()

    def remover_no(self):
        chave = int(self.entrada.get())
        self.arvore.remover(chave)
        self.desenhar_arvore()

    def resetar_arvore(self):
        self.arvore.resetar_arvore()
        self.desenhar_arvore()

    def desenhar_arvore(self):
        if self.canvas_figura_agg:
            self.canvas_figura_agg.get_tk_widget().grid_forget()

        G = nx.DiGraph()
        posicoes = {}

        def adicionar_arestas(no, posicoes, x=0, y=0, camada=1):
            if no:
                balanceamento = self.arvore.calcular_balanceamento(no)
                G.add_node(no.valor, label=f"{no.valor}\n({balanceamento})")
                posicoes[no.valor] = (x, y)

                if no.esquerda and no.valor != no.esquerda.valor:
                    G.add_edge(no.valor, no.esquerda.valor)
                    adicionar_arestas(no.esquerda, posicoes, x - 1 / (camada * 2), y - 1, camada + 1)

                if no.direita and no.valor != no.direita.valor:
                    G.add_edge(no.valor, no.direita.valor)
                    adicionar_arestas(no.direita, posicoes, x + 1 / (camada * 2), y - 1, camada + 1)

        adicionar_arestas(self.arvore.raiz, posicoes)

        fig, ax = plt.subplots(figsize=(8, 8))
        nx.draw(G, posicoes, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_size=1100, node_color="skyblue", ax=ax, arrows=False)

        self.canvas_figura_agg = FigureCanvasTkAgg(fig, master=self.janela)
        self.canvas_figura_agg.draw()
        self.canvas_figura_agg.get_tk_widget().grid(row=0, column=0, columnspan=3)

        plt.close(fig)

    def exibir_rotacao(self, no_original, no_novo, tipo_rotacao):
        # Desenhar a árvore com os nós em destaque
        G = nx.DiGraph()
        posicoes = {}

        def adicionar_arestas_rotacao(no, posicoes, x=0, y=0, camada=1):
            if no:
                balanceamento = self.arvore.calcular_balanceamento(no)
                cor_no = "skyblue"
                if no == no_original:
                    cor_no = "orange"  # Nó original em destaque
                elif no == no_novo:
                    cor_no = "green"  # Nó novo em destaque

                G.add_node(no.valor, label=f"{no.valor}\n({balanceamento})", color=cor_no)
                posicoes[no.valor] = (x, y)

                if no.esquerda and no.valor != no.esquerda.valor:
                    G.add_edge(no.valor, no.esquerda.valor)
                    adicionar_arestas_rotacao(no.esquerda, posicoes, x - 1 / (camada * 2), y - 1, camada + 1)

                if no.direita and no.valor != no.direita.valor:
                    G.add_edge(no.valor, no.direita.valor)
                    adicionar_arestas_rotacao(no.direita, posicoes, x + 1 / (camada * 2), y - 1, camada + 1)

        adicionar_arestas_rotacao(self.arvore.raiz, posicoes)

        fig, ax = plt.subplots(figsize=(8, 8))
        cores = [G.nodes[n]['color'] for n in G.nodes]
        nx.draw(G, posicoes, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_size=1100, node_color=cores, ax=ax, arrows=False)

        self.canvas_figura_agg = FigureCanvasTkAgg(fig, master=self.janela)
        self.canvas_figura_agg.draw()
        self.canvas_figura_agg.get_tk_widget().grid(row=0, column=0, columnspan=3)

        plt.close(fig)

        # Exibir mensagem de rotação
        tk.messagebox.showinfo("Rotação AVL", f"Tipo de Rotação: {tipo_rotacao}")

        # Esperar 4 segundos antes de redibujar a árvore
        self.janela.update_idletasks()
        #time.sleep(4)

        # Redesenhar a árvore completa sem destaque
        self.desenhar_arvore()

    def salvar_e_sair(self):
        self.arvore.salvar_arvore(self.caminho_arquivo)
        self.janela.destroy()

if __name__ == "__main__":
    app = InterfaceArvoreAVL()
