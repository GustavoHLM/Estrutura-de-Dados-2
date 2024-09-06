#pip install matplotlib, instale para usar a lib que desenha Grafos
import tkinter as tk  # Importa o módulo tkinter para criar a interface gráfica
from tkinter import Canvas  # Importa o Canvas do tkinter para desenhar na janela
import networkx as nx  # Importa o NetworkX para criar e manipular grafos
import matplotlib.pyplot as plt  # Importa o matplotlib para plotar o grafo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Importa o FigureCanvasTkAgg para integrar matplotlib com tkinter

# Classe Nó que representa cada nó na árvore binária
class No:
    def __init__(self, chave):
        self.esquerda = None  # Inicializa o ponteiro para o filho à esquerda como None
        self.direita = None  # Inicializa o ponteiro para o filho à direita como None
        self.valor = chave  # Armazena o valor da chave no nó

class ArvoreBinaria:
    def __init__(self, raiz):
        self.raiz = No(raiz)  # Inicializa a árvore com um nó raiz

    def inserir(self, chave):
        self.raiz = self._inserir(self.raiz, chave)  # Chama o método privado _inserir para adicionar a chave na árvore
        
    def _inserir(self, raiz, chave):
        if raiz is None:  # Se o nó atual for None, cria um novo nó com a chave
            return No(chave)
        else:
            if chave == raiz.valor:  # Se a chave já existir, não insere o nó
                return raiz  # Retorna a raiz sem modificações
            elif chave < raiz.valor:  # Se a chave for menor que o valor do nó atual, insere na subárvore esquerda
                raiz.esquerda = self._inserir(raiz.esquerda, chave)
            else:  # Se a chave for maior que o valor do nó atual, insere na subárvore direita
                raiz.direita = self._inserir(raiz.direita, chave)
        return raiz  # Retorna a raiz atualizada

    def remover(self, chave):
        self.raiz = self._remover(self.raiz, chave)  # Chama o método privado _remover para remover a chave da árvore
        
    def _remover(self, raiz, chave):
        if raiz is None:  # Se o nó atual for None, retorna None
            return raiz
        
        if chave < raiz.valor:  # Se a chave for menor que o valor do nó atual, busca na subárvore esquerda
            raiz.esquerda = self._remover(raiz.esquerda, chave)
        elif chave > raiz.valor:  # Se a chave for maior que o valor do nó atual, busca na subárvore direita
            raiz.direita = self._remover(raiz.direita, chave)
        else:  # Se a chave for igual ao valor do nó atual, encontrou o nó a ser removido
            if raiz.esquerda is None:  # Se o nó não tem filho à esquerda, retorna o filho à direita
                return raiz.direita
            elif raiz.direita is None:  # Se o nó não tem filho à direita, retorna o filho à esquerda
                return raiz.esquerda
            
            # Se o nó tem dois filhos, encontra o menor valor na subárvore direita
            menor_no_maior_subarvore = self._minimo_valor_no(raiz.direita)
            raiz.valor = menor_no_maior_subarvore.valor  # Substitui o valor do nó atual pelo menor valor encontrado
            raiz.direita = self._remover(raiz.direita, menor_no_maior_subarvore.valor)  # Remove o nó de menor valor
        
        return raiz  # Retorna a raiz atualizada

    def _minimo_valor_no(self, no):
        atual = no  # Inicializa o nó atual
        while atual.esquerda is not None:  # Percorre até o nó mais à esquerda
            atual = atual.esquerda
        return atual  # Retorna o nó de menor valor

# Classe InterfaceArvoreBinaria para criar a interface gráfica e interagir com a árvore binária
class InterfaceArvoreBinaria:
    def __init__(self, raiz):
        self.arvore = ArvoreBinaria(raiz)  # Inicializa a árvore binária com a raiz fornecida
        
        self.janela = tk.Tk()  # Cria a janela principal
        self.janela.title("Árvore Binária")  # Define o título da janela
        
        # Cria um Canvas para desenhar a árvore
        self.canvas = Canvas(self.janela, width=800, height=500)
        self.canvas.grid(row=0, column=0, columnspan=2)  # Posiciona o Canvas na janela

        # Cria uma caixa de entrada para receber o valor do nó
        self.entrada = tk.Entry(self.janela)
        self.entrada.grid(row=1, column=0, padx=2, pady=2)  # Posiciona a entrada na janela
        
        # Cria um botão para adicionar um nó à árvore
        self.botao_adicionar = tk.Button(self.janela, text="Adicionar Nó", command=self.adicionar_no)
        self.botao_adicionar.grid(row=1, column=1, padx=2, pady=2)  # Posiciona o botão na janela

        # Cria um botão para remover um nó da árvore
        self.botao_remover = tk.Button(self.janela, text="Remover Nó", command=self.remover_no)
        self.botao_remover.grid(row=1, column=0, columnspan=2, padx=2, pady=2)  # Posiciona o botão na janela
        
        self.canvas_figura_agg = None  # Inicializa o canvas do matplotlib como None
        
        self.desenhar_arvore()  # Desenha a árvore inicialmente
        
        self.janela.mainloop()  # Inicia o loop principal da interface gráfica
    
    def adicionar_no(self):
        chave = int(self.entrada.get())  # Obtém a chave inserida pelo usuário
        self.arvore.inserir(chave)  # Insere a chave na árvore
        self.desenhar_arvore()  # Redesenha a árvore
    
    def remover_no(self):
        chave = int(self.entrada.get())  # Obtém a chave inserida pelo usuário
        self.arvore.remover(chave)  # Remove a chave da árvore
        self.desenhar_arvore()  # Redesenha a árvore
        
    def desenhar_arvore(self):
        if self.canvas_figura_agg:  # Se já existe um gráfico, remove-o
            self.canvas_figura_agg.get_tk_widget().grid_forget()
        
        G = nx.DiGraph()  # Cria um novo grafo direcionado
        posicoes = {}  # Dicionário para armazenar as posições dos nós
        
        # Função recursiva para adicionar arestas e posições ao grafo
        def adicionar_arestas(no, posicoes, x=0, y=0, camada=1):
            if no:
                G.add_node(no.valor)  # Adiciona o nó ao grafo
                posicoes[no.valor] = (x, y)  # Define a posição do nó
                
                # Verifica e adiciona aresta para o filho à esquerda, se o valor for diferente
                if no.esquerda and no.valor != no.esquerda.valor:
                    G.add_edge(no.valor, no.esquerda.valor)  # Adiciona a aresta
                    adicionar_arestas(no.esquerda, posicoes, x - 1/(camada*2), y - 1, camada + 1)
                
                # Verifica e adiciona aresta para o filho à direita, se o valor for diferente
                if no.direita and no.valor != no.direita.valor:
                    G.add_edge(no.valor, no.direita.valor)  # Adiciona a aresta
                    adicionar_arestas(no.direita, posicoes, x + 1/(camada*2), y - 1, camada + 1)

        
        adicionar_arestas(self.arvore.raiz, posicoes)  # Adiciona as arestas e posições começando pela raiz
        
        fig, ax = plt.subplots(figsize=(8, 6))  # Cria uma figura para desenhar o grafo
        nx.draw(G, posicoes, with_labels=True, node_size=700, node_color="skyblue", ax=ax, arrows=False)  # Desenha o grafo
        
        self.canvas_figura_agg = FigureCanvasTkAgg(fig, master=self.janela)  # Cria o canvas do matplotlib
        self.canvas_figura_agg.draw()  # Desenha o canvas
        self.canvas_figura_agg.get_tk_widget().grid(row=0, column=0, columnspan=2)  # Posiciona o gráfico na janela
        
        plt.close(fig)  # Fecha a figura para liberar memória

if __name__ == "__main__":
    app = InterfaceArvoreBinaria(10)  # Cria uma instância da interface gráfica com a raiz inicial de valor 10
