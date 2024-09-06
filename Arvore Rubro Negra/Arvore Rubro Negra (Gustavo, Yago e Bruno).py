import tkinter as tk
from tkinter import Canvas
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle
import os


class No:
    def __init__(self, valor):
        self.valor = valor  # Valor armazenado no nó
        self.esquerda = None  # Referência para o filho à esquerda
        self.direita = None  # Referência para o filho à direita
        self.pai = None  # Referência para o pai do nó
        self.cor = "vermelho"  # Cor inicial do nó, que é vermelho por padrão

class ArvoreRubroNegra:
    def __init__(self):
        self.raiz = None  # Inicialmente, a árvore está vazia

    def inserir(self, valor):
        novo_no = No(valor)  # Cria um novo nó com o valor especificado
        self._inserir_no(self.raiz, novo_no)  # Insere o nó na árvore
        self._ajustar_insercao(novo_no)  # Ajusta a árvore para manter as propriedades da árvore rubro-negra

    def _inserir_no(self, raiz, novo_no):
        if not self.raiz:
            self.raiz = novo_no  # Se a árvore estiver vazia, o novo nó é a raiz
            self.raiz.cor = "preto"  # A raiz deve ser preta
        else:
            if novo_no.valor < raiz.valor:
                if raiz.esquerda:
                    self._inserir_no(raiz.esquerda, novo_no)  # Recurre para a subárvore esquerda
                else:
                    raiz.esquerda = novo_no  # Adiciona o novo nó como filho à esquerda
                    novo_no.pai = raiz  # Define o pai do novo nó
            elif novo_no.valor > raiz.valor:
                if raiz.direita:
                    self._inserir_no(raiz.direita, novo_no)  # Recurre para a subárvore direita
                else:
                    raiz.direita = novo_no  # Adiciona o novo nó como filho à direita
                    novo_no.pai = raiz  # Define o pai do novo nó

    def _ajustar_insercao(self, no):
        while no != self.raiz and no.pai.cor == "vermelho":
            if no.pai == no.pai.pai.esquerda:
                tio = no.pai.pai.direita  # Tio do nó
                if tio and tio.cor == "vermelho":
                    no.pai.cor = "preto"  # Se o tio for vermelho, realiza uma mudança de cor
                    tio.cor = "preto"
                    no.pai.pai.cor = "vermelho"
                    no = no.pai.pai  # Move para o avô
                else:
                    if no == no.pai.direita:
                        no = no.pai
                        self._rotacao_esquerda(no)  # Se o nó for filho direito, realiza uma rotação esquerda
                    no.pai.cor = "preto"
                    no.pai.pai.cor = "vermelho"
                    self._rotacao_direita(no.pai.pai)  # Realiza a rotação direita no avô
            else:
                tio = no.pai.pai.esquerda  # Caso simétrico ao anterior, mas para a subárvore direita
                if tio and tio.cor == "vermelho":
                    no.pai.cor = "preto"
                    tio.cor = "preto"
                    no.pai.pai.cor = "vermelho"
                    no = no.pai.pai
                else:
                    if no == no.pai.esquerda:
                        no = no.pai
                        self._rotacao_direita(no)
                    no.pai.cor = "preto"
                    no.pai.pai.cor = "vermelho"
                    self._rotacao_esquerda(no.pai.pai)
        self.raiz.cor = "preto"  # Garante que a raiz seja preta

    def _rotacao_esquerda(self, no):
        y = no.direita  # Nó que vai subir
        no.direita = y.esquerda  # Substitui o filho direito do nó
        if y.esquerda:
            y.esquerda.pai = no  # Ajusta o pai do novo filho à direita
        y.pai = no.pai  # Ajusta o pai de y
        if not no.pai:
            self.raiz = y  # Se o nó for a raiz, y se torna a nova raiz
        elif no == no.pai.esquerda:
            no.pai.esquerda = y  # Ajusta o pai do nó
        else:
            no.pai.direita = y
        y.esquerda = no  # Faz a rotação
        no.pai = y

    def _rotacao_direita(self, no):
        y = no.esquerda  # Nó que vai subir
        no.esquerda = y.direita  # Substitui o filho esquerdo do nó
        if y.direita:
            y.direita.pai = no  # Ajusta o pai do novo filho à esquerda
        y.pai = no.pai  # Ajusta o pai de y
        if not no.pai:
            self.raiz = y  # Se o nó for a raiz, y se torna a nova raiz
        elif no == no.pai.direita:
            no.pai.direita = y  # Ajusta o pai do nó
        else:
            no.pai.esquerda = y
        y.direita = no  # Faz a rotação
        no.pai = y

    def remover(self, chave):
        no_a_remover = self._buscar_no(self.raiz, chave)  # Busca o nó a ser removido
        if no_a_remover:
            self._remover(no_a_remover)  # Remove o nó encontrado

    def _buscar_no(self, no, chave):
        if no is None or chave == no.valor:
            return no  # Retorna o nó se encontrado
        if chave < no.valor:
            return self._buscar_no(no.esquerda, chave)  # Busca na subárvore esquerda
        else:
            return self._buscar_no(no.direita, chave)  # Busca na subárvore direita

    def _remover(self, no):
        original_cor = no.cor  # Guarda a cor original do nó
        if no.esquerda is None:
            substituto = no.direita
            self._transplantar(no, substituto)  # Substitui o nó removido por seu filho direito
        elif no.direita is None:
            substituto = no.esquerda
            self._transplantar(no, substituto)  # Substitui o nó removido por seu filho esquerdo
        else:
            sucessor = self._minimo(no.direita)  # Encontra o sucessor in-order
            original_cor = sucessor.cor
            substituto = sucessor.direita
            if sucessor.pai == no:
                if substituto:
                    substituto.pai = sucessor
            else:
                self._transplantar(sucessor, sucessor.direita)
                sucessor.direita = no.direita
                sucessor.direita.pai = sucessor
            self._transplantar(no, sucessor)
            sucessor.esquerda = no.esquerda
            sucessor.esquerda.pai = sucessor
            sucessor.cor = no.cor

        if original_cor == "preto":
            self._ajustar_remocao(substituto)  # Ajusta a árvore após a remoção

    def _transplantar(self, u, v):
        if u.pai is None:
            self.raiz = v  # Substitui a raiz se necessário
        elif u == u.pai.esquerda:
            u.pai.esquerda = v
        else:
            u.pai.direita = v
        if v:
            v.pai = u.pai  # Ajusta o pai do nó substituto

    def _minimo(self, no):
        while no.esquerda:
            no = no.esquerda  # Encontra o nó mais à esquerda (mínimo)
        return no

    def _ajustar_remocao(self, no):
        while no != self.raiz and (no is None or no.cor == "preto"):
            if no is not None and no.pai is not None:  # Verifica se o nó e o pai existem
                if no == no.pai.esquerda:
                    irmao = no.pai.direita  # Irmão do nó
                    if irmao and irmao.cor == "vermelho":
                        irmao.cor = "preto"
                        no.pai.cor = "vermelho"
                        self._rotacao_esquerda(no.pai)  # Ajusta a árvore se o irmão for vermelho
                        irmao = no.pai.direita
                    if (irmao is None or (irmao.esquerda is None or irmao.esquerda.cor == "preto") and
                            (irmao.direita is None or irmao.direita.cor == "preto")):
                        if irmao:
                            irmao.cor = "vermelho"
                        no = no.pai
                    else:
                        if irmao and (irmao.direita is None or irmao.direita.cor == "preto"):
                            if irmao.esquerda:
                                irmao.esquerda.cor = "preto"
                            if irmao:
                                irmao.cor = "vermelho"
                            self._rotacao_direita(irmao)
                            irmao = no.pai.direita
                        if irmao:
                            irmao.cor = no.pai.cor
                        no.pai.cor = "preto"
                        if irmao and irmao.direita:
                            irmao.direita.cor = "preto"
                        self._rotacao_esquerda(no.pai)
                        no = self.raiz
                else:
                    irmao = no.pai.esquerda
                    if irmao and irmao.cor == "vermelho":
                        irmao.cor = "preto"
                        no.pai.cor = "vermelho"
                        self._rotacao_direita(no.pai)
                        irmao = no.pai.esquerda
                    if (irmao is None or (irmao.direita is None or irmao.direita.cor == "preto") and
                            (irmao.esquerda is None or irmao.esquerda.cor == "preto")):
                        if irmao:
                            irmao.cor = "vermelho"
                        no = no.pai
                    else:
                        if irmao and (irmao.esquerda is None or irmao.esquerda.cor == "preto"):
                            if irmao.direita:
                                irmao.direita.cor = "preto"
                            if irmao:
                                irmao.cor = "vermelho"
                            self._rotacao_esquerda(irmao)
                            irmao = no.pai.esquerda
                        if irmao:
                            irmao.cor = no.pai.cor
                        no.pai.cor = "preto"
                        if irmao and irmao.esquerda:
                            irmao.esquerda.cor = "preto"
                        self._rotacao_direita(no.pai)
                        no = self.raiz
            else:
                break  # Sai do loop se no ou no.pai forem None
        if no:
            no.cor = "preto"  # Garante que o nó final seja preto

    def resetar_arvore(self):
        self.raiz = None  # Reseta a árvore para o estado inicial (vazia)

    def copiar_estado(self):
        nova_arvore = ArvoreRubroNegra()
        nova_arvore.raiz = self._copiar_no(self.raiz)  # Cria uma nova árvore com uma cópia dos nós
        return nova_arvore

    def _copiar_no(self, no):
        if no is None:
            return None
        novo_no = No(no.valor)
        novo_no.cor = no.cor
        novo_no.esquerda = self._copiar_no(no.esquerda)
        novo_no.direita = self._copiar_no(no.direita)
        if novo_no.esquerda:
            novo_no.esquerda.pai = novo_no
        if novo_no.direita:
            novo_no.direita.pai = novo_no
        return novo_no

    def salvar_arvore(self, caminho):
        with open(caminho, 'wb') as f:
            pickle.dump(self, f)  # Serializa e salva a árvore em um arquivo

    def carregar_arvore(self, caminho):
        if os.path.exists(caminho):
            with open(caminho, 'rb') as f:
                arvore_carregada = pickle.load(f)  # Carrega a árvore a partir de um arquivo
                self.raiz = arvore_carregada.raiz


class InterfaceArvoreRubroNegra:
    def __init__(self):
        self.caminho_arquivo = 'arvore_rubro_negra.bin'
        self.arvore = ArvoreRubroNegra()
        self.arvore.carregar_arvore(self.caminho_arquivo)
        self.arvore_anterior = self.arvore.copiar_estado()

        self.janela = tk.Tk()
        self.janela.title("Árvore Rubro-Negra")

        self.canvas = Canvas(self.janela, width=1280, height=720)
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

        self.desenhar_arvores()

        self.janela.protocol("WM_DELETE_WINDOW", self.salvar_e_sair)

        self.janela.mainloop()

    def adicionar_no(self):
        self.arvore_anterior = self.arvore.copiar_estado()
        chave = int(self.entrada.get())
        self.arvore.inserir(chave)
        self.desenhar_arvores()

    def remover_no(self):
        self.arvore_anterior = self.arvore.copiar_estado()
        chave = int(self.entrada.get())
        self.arvore.remover(chave)
        self.desenhar_arvores()

    def resetar_arvore(self):
        self.arvore.resetar_arvore()
        self.arvore_anterior = ArvoreRubroNegra()  # Reseta também a árvore anterior
        self.desenhar_arvores()

    def desenhar_arvores(self):
        if self.canvas_figura_agg:
            self.canvas_figura_agg.get_tk_widget().grid_forget()

        fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # Cria dois gráficos lado a lado

        def desenhar_no_grafico(arvore, ax):
            G = nx.DiGraph()
            posicoes = {}

            def adicionar_arestas(no, posicoes, x=0, y=0, camada=1):
                if no:
                    cor_no = "red" if no.cor == "vermelho" else "black"
                    G.add_node(no.valor, label=f"{no.valor}", color=cor_no)
                    posicoes[no.valor] = (x, y)

                    if no.esquerda and no.valor != no.esquerda.valor:
                        G.add_edge(no.valor, no.esquerda.valor)
                        adicionar_arestas(no.esquerda, posicoes, x - 1 / (camada * 2), y - 1, camada + 1)

                    if no.direita and no.valor != no.direita.valor:
                        G.add_edge(no.valor, no.direita.valor)
                        adicionar_arestas(no.direita, posicoes, x + 1 / (camada * 2), y - 1, camada + 1)

            adicionar_arestas(arvore.raiz, posicoes)
            cores = [G.nodes[n]['color'] for n in G.nodes()]
            nx.draw(G, pos=posicoes, labels=nx.get_node_attributes(G, 'label'), ax=ax, node_color=cores, with_labels=True, node_size=500, font_color="white", font_size=10, font_weight="bold")
            ax.set_xlim(-1, 1)
            ax.set_ylim(-len(posicoes), 1)
            ax.axis('off')

        desenhar_no_grafico(self.arvore_anterior, axs[0])  # Desenha o estado anterior
        axs[0].set_title("Estado Anterior")

        desenhar_no_grafico(self.arvore, axs[1])  # Desenha o estado atual
        axs[1].set_title("Estado Atual")

        self.canvas_figura_agg = FigureCanvasTkAgg(fig, master=self.janela)
        self.canvas_figura_agg.draw()
        self.canvas_figura_agg.get_tk_widget().grid(row=0, column=0, columnspan=3)

        plt.close(fig)

    def salvar_e_sair(self):
        self.arvore.salvar_arvore(self.caminho_arquivo)
        self.janela.destroy()

if __name__ == "__main__":
    InterfaceArvoreRubroNegra()
