class Nodo:
    def __init__(self, chave):
        # Inicializa o nodo com a chave fornecida
        self.chave = chave
        # Inicialmente, o nodo não tem filhos, então ambos são None
        self.esquerda = None
        self.direita = None

class ArvoreBinaria:
    def __init__(self):
        # Inicializa a árvore com a raiz como None, indicando que a árvore está vazia
        self.raiz = None

    def inserir(self, chave):
        # Método público para inserir uma nova chave na árvore
        # Se a árvore estiver vazia, cria a raiz com a nova chave
        if self.raiz is None:
            self.raiz = Nodo(chave)
        else:
            # Caso contrário, chama o método auxiliar para inserir a chave na posição correta
            self._inserir(chave, self.raiz)

    def _inserir(self, chave, nodo_atual):
        # Método auxiliar recursivo para inserir uma chave na árvore

        # Se a chave for menor que a chave do nodo atual, vai para a subárvore esquerda
        if chave < nodo_atual.chave:
            # Se o nodo esquerdo for None, insere a chave aqui
            if nodo_atual.esquerda is None:
                nodo_atual.esquerda = Nodo(chave)
            else:
                # Caso contrário, continua a busca recursivamente na subárvore esquerda
                self._inserir(chave, nodo_atual.esquerda)
        # Se a chave for maior que a chave do nodo atual, vai para a subárvore direita
        elif chave > nodo_atual.chave:
            # Se o nodo direito for None, insere a chave aqui
            if nodo_atual.direita is None:
                nodo_atual.direita = Nodo(chave)
            else:
                # Caso contrário, continua a busca recursivamente na subárvore direita
                self._inserir(chave, nodo_atual.direita)

    def remover(self, chave):
        # Método público para remover uma chave da árvore
        # Inicia a remoção chamando o método auxiliar a partir da raiz
        self.raiz = self._remover(chave, self.raiz)

    def _remover(self, chave, nodo_atual):
        # Método auxiliar recursivo para remover uma chave da árvore

        # Se o nodo atual for None, a chave não está na árvore
        if nodo_atual is None:
            return nodo_atual

        # Se a chave a ser removida for menor que a chave do nodo atual, busca na subárvore esquerda
        if chave < nodo_atual.chave:
            nodo_atual.esquerda = self._remover(chave, nodo_atual.esquerda)
        # Se a chave a ser removida for maior que a chave do nodo atual, busca na subárvore direita
        elif chave > nodo_atual.chave:
            nodo_atual.direita = self._remover(chave, nodo_atual.direita)
        else:
            # Nodo encontrado: agora, precisa ser removido

            # Caso 1: Nodo com apenas um filho ou nenhum
            if nodo_atual.esquerda is None:
                return nodo_atual.direita
            elif nodo_atual.direita is None:
                return nodo_atual.esquerda

            # Caso 2: Nodo com dois filhos, obtém o sucessor (menor nodo da subárvore direita)
            temp = self._min_value_node(nodo_atual.direita)
            # Copia a chave do sucessor para o nodo atual
            nodo_atual.chave = temp.chave
            # Remove o sucessor na subárvore direita
            nodo_atual.direita = self._remover(temp.chave, nodo_atual.direita)

        return nodo_atual

    def _min_value_node(self, nodo):
        # Método auxiliar para encontrar o nodo com o menor valor (mais à esquerda) na árvore/subárvore
        atual = nodo
        # Continua a busca pelo menor valor até encontrar o nodo mais à esquerda
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def mostrar(self):
        # Método público para mostrar a estrutura completa da árvore
        # Se a árvore não estiver vazia, chama o método auxiliar para mostrar a árvore
        if self.raiz is not None:
            self._mostrar(self.raiz)

    def _mostrar(self, nodo_atual, nivel=0):
        # Método auxiliar recursivo para mostrar a árvore
        if nodo_atual is not None:
            # Primeiramente, mostra a subárvore direita (com indentação adicional)
            self._mostrar(nodo_atual.direita, nivel + 1)
            # Exibe o nodo atual com indentação correspondente ao nível
            print(' ' * 4 * nivel + '->', nodo_atual.chave)
            # Finalmente, mostra a subárvore esquerda (com indentação adicional)
            self._mostrar(nodo_atual.esquerda, nivel + 1)

if __name__ == "__main__":
    # Código principal que executa a interação com o usuário

    # Cria uma instância da árvore binária
    arvore = ArvoreBinaria()

    # Loop principal do programa
    while True:
        # Exibe o menu de opções para o usuário
        print("\nMenu:")
        print("1. Inserir valor na árvore")
        print("2. Remover valor da árvore")
        print("3. Exibir árvore completa")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            # Inserir valor na árvore
            while True:
                # Pede ao usuário para inserir um valor
                valor = input("Digite um valor para inserir (ou 'x' para parar): ")
                # Se o usuário digitar 'x', o loop de inserção para
                if valor == 'x':
                    break
                try:
                    # Tenta converter o valor inserido para inteiro e insere na árvore
                    arvore.inserir(int(valor))
                except ValueError:
                    # Se a conversão falhar, informa ao usuário que o valor deve ser numérico
                    print("Por favor, insira um valor numérico válido.")

        elif opcao == '2':
            # Remover valor da árvore
            while True:
                # Pede ao usuário para remover um valor
                valor = input("Digite um valor para remover (ou 'x' para parar): ")
                # Se o usuário digitar 'x', o loop de remoção para
                if valor == 'x':
                    break
                try:
                    # Tenta converter o valor inserido para inteiro e remove da árvore
                    arvore.remover(int(valor))
                except ValueError:
                    # Se a conversão falhar, informa ao usuário que o valor deve ser numérico
                    print("Por favor, insira um valor numérico válido.")

        elif opcao == '3':
            # Exibir árvore completa
            print("\nÁrvore completa:")
            # Chama o método para mostrar a árvore
            arvore.mostrar()

        elif opcao == '4':
            # Sair do programa
            print("Saindo...")
            # Interrompe o loop principal, encerrando o programa
            break

        else:
            # Se o usuário inserir uma opção inválida, exibe uma mensagem de erro
            print("Opção inválida. Tente novamente.")