import tkinter as tk  # Importa o módulo tkinter para criar interfaces gráficas.
from tkinter import Canvas  # Importa a classe Canvas para desenhar gráficos na interface.
from tkinter import messagebox  # Importa a classe messagebox para exibir caixas de diálogo.
import json  # Importa o módulo json para manipulação de arquivos JSON.
import os  # Importa o módulo os para manipulação de diretórios e arquivos.

# Define a classe Node, que representa um nó na árvore Rubro-Negra.
class Node:
    def __init__(self, key, color, left=None, right=None, parent=None):
        self.key = key  # Valor armazenado no nó.
        self.color = color  # Cor do nó ('red' ou 'black').
        self.left = left  # Filho à esquerda.
        self.right = right  # Filho à direita.
        self.parent = parent  # Nó pai.

# Define a classe RedBlackTree, que representa a árvore Rubro-Negra.
class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0, 'black')  # Nó sentinela usado para folhas.
        self.root = self.TNULL  # Inicialmente, a árvore está vazia.

    # Método para inserir um novo nó na árvore.
    def insert(self, key):
        new_node = Node(key, 'red', left=self.TNULL, right=self.TNULL, parent=None)  # Cria um novo nó.
        parent_node = None  # Nodo pai do novo nó.
        current_node = self.root  # Começa pela raiz.

        # Encontra o local apropriado para o novo nó.
        while current_node != self.TNULL:
            parent_node = current_node
            if new_node.key < current_node.key:
                current_node = current_node.left
            elif new_node.key > current_node.key:
                current_node = current_node.right
            else:
                # Se a chave já existe, exibe uma mensagem e retorna.
                messagebox.showinfo("Aviso", f"Chave {key} já existe na árvore.")
                return

        new_node.parent = parent_node  # Define o pai do novo nó.

        # Insere o novo nó na árvore.
        if parent_node is None:  # Se a árvore estava vazia.
            self.root = new_node
        elif new_node.key < parent_node.key:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        if new_node.parent is None:  # Se o novo nó é a raiz.
            new_node.color = 'black'  # A raiz é sempre preta.
            return

        if new_node.parent.parent is None:
            return

        # Corrige a árvore se necessário para manter as propriedades da árvore Rubro-Negra.
        self.fix_insert(new_node)

    # Método para corrigir a árvore após a inserção.
    def fix_insert(self, node):
        # Enquanto o pai do nó atual for vermelho, o que indica uma violação das propriedades da árvore Rubro-Negra.
        while node.parent.color == 'red':
            # Verifica se o pai do nó atual é o filho direito do avô (caso em que o tio está à esquerda).
            if node.parent == node.parent.parent.right:
                u = node.parent.parent.left  # O tio do nó é o filho esquerdo do avô.
                # Caso 1: O tio é vermelho.
                if u.color == 'red':
                    # Caso 1.1: Pinta o tio e o pai do nó de preto.
                    u.color = 'black'
                    node.parent.color = 'black'
                    # Pinta o avô do nó de vermelho.
                    node.parent.parent.color = 'red'
                    # Move o nó para o avô para continuar a correção se necessário.
                    node = node.parent.parent
                else:
                    # Caso 2: O tio é preto.
                    # Se o nó é o filho esquerdo do pai, realiza uma rotação à direita.
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    # Pinta o pai de preto e o avô de vermelho.
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    # Realiza uma rotação à esquerda no avô do nó para manter a propriedade da árvore Rubro-Negra.
                    self.left_rotate(node.parent.parent)
            else:
                # Simetria: o pai do nó atual é o filho esquerdo do avô (caso em que o tio está à direita).
                u = node.parent.parent.right  # O tio do nó é o filho direito do avô.
                # Caso 1: O tio é vermelho.
                if u.color == 'red':
                    # Caso 1.1: Pinta o tio e o pai do nó de preto.
                    u.color = 'black'
                    node.parent.color = 'black'
                    # Pinta o avô do nó de vermelho.
                    node.parent.parent.color = 'red'
                    # Move o nó para o avô para continuar a correção se necessário.
                    node = node.parent.parent
                else:
                    # Caso 2: O tio é preto.
                    # Se o nó é o filho direito do pai, realiza uma rotação à esquerda.
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    # Pinta o pai de preto e o avô de vermelho.
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    # Realiza uma rotação à direita no avô do nó para manter a propriedade da árvore Rubro-Negra.
                    self.right_rotate(node.parent.parent)
            # Se o nó atual se tornou a raiz, a correção é completa.
            if node == self.root:
                break
        # Garante que a raiz da árvore seja preta, conforme a propriedade da árvore Rubro-Negra.
        self.root.color = 'black'

    # Método para deletar um nó com uma determinada chave.
    def delete_node(self, key):
        self.delete_node_helper(self.root, key)

    # Método auxiliar para deletar um nó.
    def delete_node_helper(self, node, key):
        z = self.TNULL
        # Encontra o nó que deve ser deletado. O loop procura pelo nó com a chave fornecida.
        while node != self.TNULL:
            if node.key == key:
                z = node  # Nó a ser deletado encontrado.
                break
            if key < node.key:
                node = node.left  # Continua a busca na subárvore esquerda.
            else:
                node = node.right  # Continua a busca na subárvore direita.

        # Se o nó a ser deletado não foi encontrado, exibe uma mensagem de aviso e encerra o método.
        if z == self.TNULL:
            messagebox.showinfo("Aviso", f"Chave {key} não encontrada na árvore.")
            return

        y = z  # Nó que será usado para substituir o nó z.
        y_original_color = y.color  # Guarda a cor original de y para tratar o caso de remoção de um nó preto.
        # Caso 1: O nó a ser deletado não tem filho esquerdo.
        if z.left == self.TNULL:
            x = z.right  # O nó filho direito de z será substituto de z.
            self.rb_transplant(z, z.right)  # Substitui z por seu filho direito.
        # Caso 2: O nó a ser deletado não tem filho direito.
        elif z.right == self.TNULL:
            x = z.left  # O nó filho esquerdo de z será substituto de z.
            self.rb_transplant(z, z.left)  # Substitui z por seu filho esquerdo.
        else:
            # Caso 3: O nó a ser deletado tem dois filhos.
            y = self.minimum(z.right)  # Encontra o nó mínimo na subárvore direita de z (sucessor em ordem).
            y_original_color = y.color  # Guarda a cor original de y.
            x = y.right  # O filho direito de y será o substituto de y.
            # Se y é um filho direto de z, atualiza o pai de x.
            if y.parent == z:
                x.parent = y
            else:
                # Substitui y por seu filho direito.
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            # Substitui z por y.
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        # Se a cor original de y era preta, corrige a árvore para manter as propriedades da árvore Rubro-Negra.
        if y_original_color == 'black':
            self.fix_delete(x)

    # Método para corrigir a árvore após a exclusão de um nó.
    def fix_delete(self, x):
        # Corrige a árvore para manter as propriedades da árvore Rubro-Negra após a exclusão.
        while x != self.root and x.color == 'black':
            # Caso 1: x é o filho esquerdo do pai.
            if x == x.parent.left:
                s = x.parent.right  # O irmão de x é o filho direito do pai.
                # Se o irmão de x é vermelho, realiza uma rotação à esquerda no pai de x.
                if s.color == 'red':
                    s.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    s = x.parent.right

                # Se ambos os filhos do irmão de x são pretos, pinta o irmão de vermelho e move x para o pai.
                if s.left.color == 'black' and s.right.color == 'black':
                    s.color = 'red'
                    x = x.parent
                else:
                    # Se o filho direito do irmão é preto, realiza uma rotação à direita no irmão.
                    if s.right.color == 'black':
                        s.left.color = 'black'
                        s.color = 'red'
                        self.right_rotate(s)
                        s = x.parent.right

                    # Pinta o irmão com a cor do pai de x, pinta o pai de preto e o filho direito do irmão de preto.
                    s.color = x.parent.color
                    x.parent.color = 'black'
                    s.right.color = 'black'
                    self.left_rotate(x.parent)
                    x = self.root
            # Caso 2: x é o filho direito do pai.
            else:
                s = x.parent.left  # O irmão de x é o filho esquerdo do pai.
                # Se o irmão de x é vermelho, realiza uma rotação à direita no pai de x.
                if s.color == 'red':
                    s.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(x.parent)
                    s = x.parent.left

                # Se ambos os filhos do irmão são pretos, pinta o irmão de vermelho e move x para o pai.
                if s.right.color == 'black' and s.left.color == 'black':
                    s.color = 'red'
                    x = x.parent
                else:
                    # Se o filho esquerdo do irmão é preto, realiza uma rotação à esquerda no irmão.
                    if s.left.color == 'black':
                        s.right.color = 'black'
                        s.color = 'red'
                        self.left_rotate(s)
                        s = x.parent.left

                    # Pinta o irmão com a cor do pai de x, pinta o pai de preto e o filho esquerdo do irmão de preto.
                    s.color = x.parent.color
                    x.parent.color = 'black'
                    s.left.color = 'black'
                    self.right_rotate(x.parent)
                    x = self.root
        # Garante que a raiz permaneça preta.
        x.color = 'black'

    # Método para substituir um nó u por um nó v.
    def rb_transplant(self, u, v):
        # Substitui o nó u pelo nó v na árvore.
        if u.parent is None:
            self.root = v  # Se u é a raiz, a nova raiz é v.
        elif u == u.parent.left:
            u.parent.left = v  # Se u é o filho esquerdo do pai, v é o novo filho esquerdo do pai.
        else:
            u.parent.right = v  # Se u é o filho direito do pai, v é o novo filho direito do pai.
        v.parent = u.parent  # Atualiza o pai de v.

    # Método para encontrar o nó com a menor chave em uma subárvore.
    def minimum(self, node):
        # Percorre a subárvore esquerda até encontrar o nó mais à esquerda, que possui a menor chave.
        while node.left != self.TNULL:
            node = node.left
        return node

    # Método para realizar uma rotação à esquerda.
    def left_rotate(self, x):
        y = x.right  # O nó y é o filho direito de x.
        x.right = y.left  # Move o filho esquerdo de y para ser o filho direito de x.
        if y.left != self.TNULL:
            y.left.parent = x  # Atualiza o pai do filho esquerdo de y.
        y.parent = x.parent  # Atualiza o pai de y.
        if x.parent is None:
            self.root = y  # Se x é a raiz, a nova raiz é y.
        elif x == x.parent.left:
            x.parent.left = y  # Atualiza o filho esquerdo do pai de x.
        else:
            x.parent.right = y  # Atualiza o filho direito do pai de x.
        y.left = x  # Faz x ser o filho esquerdo de y.
        x.parent = y  # Atualiza o pai de x.

    # Método para realizar uma rotação à direita.
    def right_rotate(self, x):
        y = x.left  # O nó y é o filho esquerdo de x.
        x.left = y.right  # Move o filho direito de y para ser o filho esquerdo de x.
        if y.right != self.TNULL:
            y.right.parent = x  # Atualiza o pai do filho direito de y.
        y.parent = x.parent  # Atualiza o pai de y.
        if x.parent is None:
            self.root = y  # Se x é a raiz, a nova raiz é y.
        elif x == x.parent.right:
            x.parent.right = y  # Atualiza o filho direito do pai de x.
        else:
            x.parent.left = y  # Atualiza o filho esquerdo do pai de x.
        y.right = x  # Faz x ser o filho direito de y.
        x.parent = y  # Atualiza o pai de x.

    # Método para imprimir a árvore.
    def print_tree(self):
        # Inicia o processo de impressão se a árvore não estiver vazia.
        if self.root != self.TNULL:
            self._print_helper(self.root, "", True)

    # Método auxiliar para imprimir a árvore.
    def _print_helper(self, node, indent, last):
        if node != self.TNULL:
            print(indent, end='')
            if last:
                print("R----", end='')
                indent += "   "
            else:
                print("L----", end='')
                indent += "|  "

            s_color = "RED" if node.color == "red" else "BLACK"  # Determina a cor do nó.
            print(f"{node.key}({s_color})")  # Imprime a chave e a cor do nó.
            # Chama recursivamente para imprimir os filhos esquerdo e direito do nó.
            self._print_helper(node.left, indent, False)
            self._print_helper(node.right, indent, True)

    # Função que converte a árvore Rubro-Negra em um dicionário para fácil serialização em JSON.
    def to_dict(self, node):
        # Verifica se o nó é o nó nulo (TNULL), caso em que retornamos None.
        if node == self.TNULL:
            return None
        # Retorna um dicionário que representa o nó atual e suas subárvores.
        return {
            "key": node.key,  # Valor da chave do nó
            "color": node.color,  # Cor do nó ("red" ou "black")
            "left": self.to_dict(node.left),  # Subárvore esquerda convertida para dicionário
            "right": self.to_dict(node.right)  # Subárvore direita convertida para dicionário
        }

    # Função que salva a árvore Rubro-Negra em um arquivo JSON.
    def save_to_json(self, file_name):
        # Define o caminho do diretório 'arvores_salvas' onde os arquivos JSON serão armazenados.
        directory = os.path.join(os.path.dirname(__file__), 'arvores_salvas')
        # Cria o diretório, se ele não existir.
        os.makedirs(directory, exist_ok=True)
        # Define o caminho completo do arquivo JSON.
        file_path = os.path.join(directory, file_name + '.json')
        # Converte a árvore para um dicionário.
        tree_dict = self.to_dict(self.root)
        # Abre o arquivo JSON para escrita e salva o dicionário no arquivo.
        with open(file_path, 'w') as json_file:
            json.dump(tree_dict, json_file, indent=4)

    # Função que carrega uma árvore Rubro-Negra a partir de um arquivo JSON.
    def load_from_json(self, file_name):
        # Define o caminho do diretório 'arvores_salvas' onde os arquivos JSON estão armazenados.
        directory = os.path.join(os.path.dirname(__file__), 'arvores_salvas')
        # Define o caminho completo do arquivo JSON.
        file_path = os.path.join(directory, file_name + '.json')
    
        # Verifica se o arquivo JSON existe. Se não existir, mostra uma mensagem de aviso.
        if not os.path.exists(file_path):
            messagebox.showinfo("Aviso", f"Arquivo {file_name}.json não encontrado em {directory}.")
            return

        # Abre o arquivo JSON para leitura e carrega o dicionário da árvore.
        with open(file_path, 'r') as json_file:
            tree_dict = json.load(json_file)
             # Converte o dicionário de volta para a árvore.
            self.root = self.dict_to_tree(tree_dict)

    # Função que converte um dicionário em uma árvore Rubro-Negra.
    def dict_to_tree(self, tree_dict, parent=None):
        # Se o dicionário for None, retornamos o nó nulo (TNULL).
        if tree_dict is None:
            return self.TNULL
        # Cria um novo nó com base no dicionário.
        node = Node(tree_dict["key"], tree_dict["color"], parent=parent)
        # Converte as subárvores esquerda e direita recursivamente.
        node.left = self.dict_to_tree(tree_dict["left"], node)
        node.right = self.dict_to_tree(tree_dict["right"], node)
        return node

    # Função que limpa a árvore, definindo a raiz como o nó nulo (TNULL).
    def clear_tree(self):
        self.root = self.TNULL

# Classe para a interface gráfica da árvore Rubro-Negra usando Tkinter.
class RedBlackTreeGUI(tk.Tk):
    def __init__(self, tree):
        # Inicializa a classe base Tk.
        super().__init__()
        # Armazena a referência para a árvore Rubro-Negra.
        self.tree = tree
        self.title("Red-Black Tree Visualization")

        # Cria um frame para os botões e campos de entrada.
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Adiciona um campo de entrada para valores.
        tk.Label(control_frame, text="Valor:").pack(side=tk.LEFT)
        self.value_entry = tk.Entry(control_frame)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # Adiciona botões para inserir e remover valores.
        tk.Button(control_frame, text="Inserir", command=self.insert_value).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Remover", command=self.remove_value).pack(side=tk.LEFT)

        # Adiciona um campo de entrada para o nome do arquivo.
        tk.Label(control_frame, text="Nome do arquivo:").pack(side=tk.LEFT, padx=5)
        self.file_name_entry = tk.Entry(control_frame)
        self.file_name_entry.pack(side=tk.LEFT, padx=5)

        # Adiciona botões para salvar, carregar e limpar a árvore.
        tk.Button(control_frame, text="Salvar", command=self.save_tree).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Carregar", command=self.load_tree).pack(side=tk.LEFT)

        tk.Button(control_frame, text="Limpar Árvore", command=self.clear_tree).pack(side=tk.LEFT)

        # Cria um canvas para desenhar a árvore.
        self.canvas = Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack()

        # Atualiza a visualização da árvore e centraliza a janela.
        self.update_tree_view()
        self.center_window()

    # Função que centraliza a janela na tela.
    def center_window(self):
        # Atualiza as tarefas pendentes para garantir que o tamanho da janela esteja correto.
        self.update_idletasks()
        # Obtém as dimensões da janela.
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # Obtém as dimensões da tela.
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcula a posição para centralizar a janela.
        position_top = int((screen_height / 2) - (window_height / 2))
        position_right = int((screen_width / 2) - (window_width / 2))

        # Ajusta a posição da janela.
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Função que insere um valor na árvore.
    def insert_value(self):
        value = int(self.value_entry.get())  # Obtém o valor do campo de entrada.
        self.tree.insert(value)  # Insere o valor na árvore.
        self.update_tree_view()  # Atualiza a visualização da árvore.

    # Função que remove um valor da árvore.
    def remove_value(self):
        value = int(self.value_entry.get())  # Obtém o valor do campo de entrada.
        self.tree.delete_node(value)  # Remove o valor da árvore.
        self.update_tree_view()  # Atualiza a visualização da árvore.

    # Função que salva a árvore em um arquivo JSON.
    def save_tree(self):
        file_name = self.file_name_entry.get()  # Obtém o nome do arquivo do campo de entrada.
        if file_name:
            self.tree.save_to_json(file_name)  # Salva a árvore no arquivo JSON.
            messagebox.showinfo("Aviso", f"Árvore salva como {file_name}.json.")
        else:
            messagebox.showinfo("Aviso", "Por favor, insira um nome para o arquivo.")

    # Função que carrega uma árvore de um arquivo JSON.
    def load_tree(self):
        file_name = self.file_name_entry.get()  # Obtém o nome do arquivo do campo de entrada.
        if file_name:
            self.tree.load_from_json(file_name)  # Carrega a árvore do arquivo JSON.
            self.update_tree_view()   # Atualiza a visualização da árvore.
            messagebox.showinfo("Aviso", f"Árvore carregada do arquivo {file_name}.json.")
        else:
            messagebox.showinfo("Aviso", "Por favor, insira um nome para o arquivo.")

    # Função que limpa a árvore atual.
    def clear_tree(self):
        self.tree.clear_tree()  # Limpa a árvore.
        self.update_tree_view()  # Atualiza a visualização da árvore.
        messagebox.showinfo("Aviso", "Árvore atual foi limpa.")

    # Função que atualiza a visualização da árvore no canvas.
    def update_tree_view(self):
        self.canvas.delete("all")  # Remove todos os itens do canvas.
        self.draw_tree(self.tree.root, 400, 30, 200)  # Desenha a árvore.


    # Função recursiva que desenha a árvore no canvas.
    def draw_tree(self, node, x, y, x_offset):
        if node != self.tree.TNULL:  # Verifica se o nó não é o nó nulo (TNULL).
            # Desenha um oval representando o nó.
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="red" if node.color == "red" else "black")
            # Adiciona o texto com o valor da chave do nó.
            self.canvas.create_text(x, y, text=str(node.key), fill="white")

            # Desenha a linha para o filho esquerdo, se existir.
            if node.left != self.tree.TNULL:
                self.canvas.create_line(x, y+20, x-x_offset, y+80)
                self.draw_tree(node.left, x-x_offset, y+80, x_offset//2)

            # Desenha a linha para o filho direito, se existir.
            if node.right != self.tree.TNULL:
                self.canvas.create_line(x, y+20, x+x_offset, y+80)
                self.draw_tree(node.right, x+x_offset, y+80, x_offset//2)

# Código de execução principal.
if __name__ == "__main__":
    rbt = RedBlackTree()  # Cria uma instância da árvore Rubro-Negra.
    app = RedBlackTreeGUI(rbt)  # Cria a interface gráfica para a árvore.
    app.mainloop()  # Inicia o loop principal da interface gráfica.
