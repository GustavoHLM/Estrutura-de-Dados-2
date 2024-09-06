class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        #Caso pra inserir na raiz
        if self.root is None:
            self.root = Node(key)
        else:
            #Caso se ja existir uma raiz
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, current_node, key):
        #Verifica se é maior ou menor que o nó
        if key < current_node.val:
            if current_node.left is None:
                current_node.left = Node(key)
            else:
                self._insert_recursive(current_node.left, key)
        else:
            #Se o nó estiver vazio
            if current_node.right is None:
                current_node.right = Node(key)
            else:
                self._insert_recursive(current_node.right, key)

    def remove(self, key):
        self.root = self._remove_recursive(self.root, key)

    def _remove_recursive(self, current_node, key):
        # se estiver na folha
        if current_node is None:
            return current_node

        #analisando se sera adicionado na esquerda ou na direita
        if key < current_node.val:
            current_node.left = self._remove_recursive(current_node.left, key)
        elif key > current_node.val:
            current_node.right = self._remove_recursive(current_node.right, key)
        else:
            # Nó com apenas um filho ou nenhum filho
            if current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left

            # Nó com dois filhos: obter o sucessor em ordem (menor na subárvore direita)
            temp = self._min_value_node(current_node.right)
            current_node.val = temp.val
            current_node.right = self._remove_recursive(current_node.right, temp.val)

        return current_node

    #menor valor dos nós
    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    #estilização
    def display(self, node=None, prefix="", is_left=True):
        if node is None:
            node = self.root

        if node.right is not None:
            new_prefix = prefix + ("│   " if is_left else "    ")
            self.display(node.right, new_prefix, False)

        print(prefix + ("└── " if is_left else "┌── ") + str(node.val))

        if node.left is not None:
            new_prefix = prefix + ("    " if is_left else "│   ")
            self.display(node.left, new_prefix, True)


if __name__ == "__main__":
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)
    bst.insert(40)
    bst.insert(60)
    bst.insert(80)

    print("Árvore Binária de Busca:")
    bst.display()

    bst.remove(20)
    print("\nÁrvore após remover 20:")
    bst.display()

    bst.remove(30)
    print("\nÁrvore após remover 30:")
    bst.display()

    bst.remove(50)
    print("\nÁrvore após remover 50:")
    bst.display()
